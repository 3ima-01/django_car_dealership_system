from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Case, DecimalField, F, Max, OuterRef, Q, Subquery, Value, When
from django.utils import timezone

from apps.autoshows.models import AutoShow
from apps.autoshows.models import Stock as AutoShowStock
from apps.common.services.base import BaseService
from apps.customers.models import Offers
from apps.suppliers.models import Discount
from apps.suppliers.models import Stock as SupplierStock


class AutoShowsService(BaseService):
    model = AutoShow

    @transaction.atomic()
    def _buy_for_autoshow(self, autoshow: AutoShow, demand):
        now = timezone.now()

        discount_id_subq = (
            Discount.objects.filter(
                supplier=OuterRef("supplier"),
                cars=OuterRef("car"),
                is_active=True,
                start_date__lte=now,
                end_date__gte=now,
            )
            .filter(Q(autoshow__isnull=True) | Q(autoshow=autoshow))
            .order_by("-start_date")
            .values("id")[:1]
        )

        discount_type_subq = Discount.objects.filter(id=OuterRef("discount_id")).values("discount_type")[:1]
        discount_value_subq = Discount.objects.filter(id=OuterRef("discount_id")).values("value")[:1]

        suitable_stocks = (
            SupplierStock.objects.select_for_update(skip_locked=True)
            .filter(quantity__gt=0)
            # annotate discount
            .annotate(
                discount_id=Subquery(discount_id_subq),
            )
            .annotate(
                disc_type=Subquery(discount_type_subq),
                disc_value=Subquery(discount_value_subq),
            )
            # calculate final price
            .annotate(
                final_price=Case(
                    When(
                        disc_type=Discount.DiscountType.PERCENT,
                        then=F("price") * (1 - F("disc_value") / Value(100, output_field=DecimalField())),
                    ),
                    When(
                        disc_type=Discount.DiscountType.FIXED,
                        then=F("price") - F("disc_value"),
                    ),
                    default=F("price"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
            .annotate(
                max_price_demand=Subquery(demand),
            )
            .annotate(autoshow_sell_price=F("final_price") * (1 + autoshow.markup_percent / Decimal("100")))
            .filter(
                final_price__gt=0,
                final_price__lte=autoshow.balance.amount,
                max_price_demand__isnull=False,
                autoshow_sell_price__lte=F("max_price_demand"),
            )
            .order_by("final_price", "id")
        )

        # 3. buy car one at the time
        purchased_car_ids = set()
        purchases = []
        for stock in suitable_stocks:
            if stock.car_id in purchased_car_ids:
                continue

            try:
                discount_obj = Discount.objects.get(id=stock.discount_id) if stock.discount_id else None

                # buy via supplier method
                sale = stock.supplier.sell_to(autoshow=autoshow, car=stock.car, discount=discount_obj)
                purchases.append((sale, stock.autoshow_sell_price))

                purchased_car_ids.add(stock.car_id)

            except (ValidationError, Discount.DoesNotExist):
                continue

        if not purchases:
            return

        for sale, autoshow_price in purchases:
            # update/create AutoShowStock
            try:
                autoshow_stock = AutoShowStock.objects.select_for_update().get(autoshow=autoshow, car=sale.car)
                autoshow_stock.quantity = F("quantity") + 1
                autoshow_stock.price = autoshow_price
                autoshow_stock.save(update_fields=["quantity", "price"])
            except AutoShowStock.DoesNotExist:
                AutoShowStock.objects.create(
                    autoshow=autoshow,
                    car=sale.car,
                    quantity=1,
                    price=autoshow_price,
                )

        # update autoshow balance
        total_spent = sum(sale.total_price.amount for sale, _ in purchases)
        autoshow.balance = autoshow.balance.amount - total_spent
        autoshow.save(update_fields=["balance"])

    def buy_cars_from_supplier(self):
        # 1. get demand
        demand = (
            Offers.objects.filter(status="ACTIVE", car_id=OuterRef("car"))
            .values("car_id")
            .annotate(max_price=Max("max_price"))
            .values("max_price")[:1]
        )

        # 2. load autoshows
        autoshows = list(
            AutoShow.objects.select_for_update().only("id", "markup_percent", "balance", "balance_currency")
        )

        if not autoshows:
            return

        # 3. each autoshow has its own transaction
        for autoshow in autoshows:
            self._buy_for_autoshow(autoshow, demand)
