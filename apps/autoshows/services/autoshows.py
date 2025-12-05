from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction
from django.db.models import F, Max, OuterRef, QuerySet, Subquery
from django.shortcuts import get_object_or_404

from apps.autoshows.models import AutoShows, AutoShowsStock
from apps.customers.models import Offers
from apps.suppliers.models import SuppliersSales, SuppliersStock


class AutoShowsService:
    def __init__(self):
        self.model = AutoShows

    def get_all(self) -> QuerySet[AutoShows]:
        return self.model.objects.all()

    def get_by_filter(self, **kwargs) -> QuerySet:
        return self.model.objects.filter(**kwargs)

    def get_by_filter_or_404(self, **kwargs) -> AutoShows:
        return get_object_or_404(self.model, **kwargs)

    def create(self, auto_show_data: dict[str, Any]):
        return self.model.objects.create(**auto_show_data)

    def update(self, auto_show_id: UUID, auto_show_data: dict[str, Any]):
        try:
            instance = self.model.objects.get(id=auto_show_id)
        except self.model.DoesNotExist:
            return

        for field, value in auto_show_data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)

        instance.save()

        return instance

    def soft_delete(self, auto_show_id: UUID):
        return self.model.objects.filter(id=auto_show_id).update(is_active="False")

    @transaction.atomic()
    def _buy_for_autoshow(self, autoshow: AutoShows, demand):
        # 1. Load autoshow with lock
        autoshow = AutoShows.objects.select_for_update().get(id=autoshow.id)

        # 2.Find suitable offers from suppliers
        suitable_stocks = (
            SuppliersStock.objects.select_for_update(skip_locked=True)
            .filter(quantity__gt=0, price__lte=autoshow.balance)
            .annotate(
                max_price_demand=Subquery(demand),
            )
            .annotate(autoshow_sell_price=F("price") * (1 + autoshow.markup_percent / Decimal("100")))
            .filter(max_price_demand__isnull=False, autoshow_sell_price__lte=F("max_price_demand"))
            .order_by("price", "id")
        )

        # 3. Buy car one at the time
        purchased_car_ids = set()
        purchases = []

        for stock in suitable_stocks:
            if stock.car_id in purchased_car_ids:
                continue  # Already bought this model for this autoshow

            purchases.append((stock, stock.autoshow_sell_price))
            purchased_car_ids.add(stock.car_id)

        if not purchases:
            return

        # 4. Batch processing of purchases
        stock_ids_to_decr = [stock.id for stock, _ in purchases]
        sales_to_create = []
        autoshow_stock_updates = []
        autoshow_stock_creates = []

        # Update supplier quantity with one request
        SuppliersStock.objects.filter(id__in=stock_ids_to_decr).update(quantity=F("quantity") - 1)

        for stock, sell_price in purchases:
            # Sale from supplier to autoshow
            sales_to_create.append(
                SuppliersSales(
                    supplier=stock.supplier,
                    autoshow=autoshow,
                    car=stock.car,
                    promotion=None,
                    total_price=stock.price,
                )
            )

            # Updating autoshow_stock
            try:
                autoshow_stock = AutoShowsStock.objects.select_for_update().get(autoshow=autoshow, car=stock.car)
                autoshow_stock.quantity = F("quantity") + 1
                autoshow_stock.price = sell_price  # Updating the price
                autoshow_stock_updates.append(autoshow_stock)
            except AutoShowsStock.DoesNotExist:
                autoshow_stock_creates.append(
                    AutoShowsStock(
                        autoshow=autoshow,
                        car=stock.car,
                        quantity=1,
                        price=sell_price,
                    )
                )

        # Bulk operations
        SuppliersSales.objects.bulk_create(sales_to_create)
        if autoshow_stock_creates:
            AutoShowsStock.objects.bulk_create(autoshow_stock_creates)
        if autoshow_stock_updates:
            AutoShowsStock.objects.bulk_update(autoshow_stock_updates, ["quantity", "price"])

        # Updating autoshow balance
        total_spent = sum(stock.price for stock, _ in purchases)
        autoshow.balance -= total_spent
        autoshow.save(update_fields=["balance"])

    def buy_cars_from_supplier(self):
        # 1. Get demand
        demand = (
            Offers.objects.filter(status="ACTIVE", car_id=OuterRef("car"))
            .values("car_id")
            .annotate(max_price=Max("max_price"))
            .values("max_price")[:1]
        )

        # 2. Load autoshows
        autoshows = list(AutoShows.objects.select_for_update().only("id", "markup_percent", "balance"))

        if not autoshows:
            return

        # 3. Each autoshow has its own transaction
        for autoshow in autoshows:
            self._buy_for_autoshow(autoshow, demand)
