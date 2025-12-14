from decimal import Decimal
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from djmoney.money import Money

from apps.accounts.models import Customers
from apps.autoshows.models import Discount
from apps.autoshows.models.autoshow import AutoShow
from apps.autoshows.models.sale import Sale
from apps.autoshows.models.stock import Stock
from apps.customers.api.exceptions.offers import (
    InsufficientFundsException,
    InvalidMaxPriceException,
    InvalidOfferStateForCancellationException,
)
from apps.customers.models import Offers, Profiles


class OffersService:
    def __init__(self):
        self.model = Offers

    def _release_reservation(self, customer: Customers, amount: Decimal):
        """Releases the reserved amount"""
        updated = Profiles.objects.filter(
            customer=customer,
            reserved_balance__gte=amount,
        ).update(
            balance=F("balance") + amount,
            reserved_balance=F("reserved_balance") - amount,
        )
        if updated == 0:
            raise InsufficientFundsException("Insufficient reserved balance for refund")

    def my_offers(self, customer_id: UUID):
        return self.model.objects.filter(customer_id=customer_id)

    def create_offer(
        self,
        customer: Customers,
        car: UUID,
        max_price: Decimal,
    ):
        if max_price <= 0:
            raise InvalidMaxPriceException

        updated = Profiles.objects.filter(
            customer=customer,
            balance__gte=max_price,
        ).update(
            balance=F("balance") - max_price,
            reserved_balance=F("reserved_balance") + max_price,
        )

        if updated == 0:
            try:
                prof = customer.profile
                available = prof.balance
            except Profiles.DoesNotExist:
                available = Decimal("0.00")
            raise InsufficientFundsException(f"Insufficient balance. Available: {available}")

        self.model.objects.create(
            customer=customer,
            car=car,
            max_price=max_price,
        )
        return "Order successfully created"

    def cancel_offer(self, offer_id: UUID, customer: Customers):
        with transaction.atomic():
            offer = Offers.objects.select_for_update().get(id=offer_id, customer=customer)
            if offer.status != "ACTIVE":
                raise InvalidOfferStateForCancellationException

            self._release_reservation(customer, offer.max_price)

            offer.status = "CANCELED"
            offer.save(update_fields=["status"])
            return "Order successfully cancelled"

    def get_by_filter_or_404(self, **kwargs):
        return get_object_or_404(self.model, **kwargs)

    def buy_car_from_autoshow(self):
        # Get all active offers
        offers = Offers.objects.filter(status="ACTIVE").select_related("customer", "car")

        for offer in offers:
            try:
                with transaction.atomic():
                    now = timezone.now()

                    # Get all available stock for the car in the offer
                    stocks = Stock.objects.filter(car=offer.car, quantity__gt=0).select_related("autoshow")

                    # Collect all available purchase options
                    stock_options = []

                    for stock in stocks:
                        # Check for applicable discounts
                        applicable_discounts = (
                            Discount.objects.filter(
                                autoshow=stock.autoshow, start_date__lte=now, end_date__gte=now, is_active=True
                            )
                            .filter(Q(cars__id=stock.car.id) | Q(cars__isnull=True))
                            .distinct()
                            .order_by("-value")  # Prefer higher discount values
                        )

                        applicable_discount = applicable_discounts.first()

                        # Calculate final price
                        final_price = stock.price

                        if applicable_discount:
                            if applicable_discount.discount_type == Discount.DiscountType.PERCENT:
                                # Apply percentage discount
                                discount_amount = stock.price.amount * (applicable_discount.value / Decimal("100"))
                                final_price = stock.price - Money(discount_amount, stock.price.currency)
                            elif applicable_discount.discount_type == Discount.DiscountType.FIXED:
                                # Apply fixed amount discount
                                discount_amount = Money(applicable_discount.value, stock.price.currency)
                                final_price = stock.price - discount_amount
                                if final_price.amount <= 0:
                                    final_price = Money("0.01", stock.price.currency)  # Minimum price

                        # Check if price is positive and within customer's budget
                        if final_price.amount > 0 and final_price <= offer.max_price:
                            stock_options.append(
                                {
                                    "stock": stock,
                                    "discount": applicable_discount,
                                    "final_price": final_price,
                                    "final_price_amount": final_price.amount,
                                }
                            )

                    # Skip if no suitable stock found
                    if not stock_options:
                        continue

                    # Sort by final price (lowest first)
                    stock_options.sort(key=lambda x: x["final_price_amount"])

                    # Select the cheapest option AFTER discount application
                    best_option = stock_options[0]
                    best_stock = best_option["stock"]
                    best_discount = best_option["discount"]
                    best_final_price = best_option["final_price"]

                    # Lock the stock record to prevent race conditions
                    stock = Stock.objects.select_for_update(skip_locked=True).get(id=best_stock.id)

                    # Verify stock is still available
                    if stock.quantity <= 0:
                        continue

                    # Lock related objects
                    autoshow = AutoShow.objects.select_for_update().get(id=stock.autoshow_id)
                    profile = Profiles.objects.select_for_update().get(customer=offer.customer)

                    # Verify customer has sufficient reserved balance
                    if profile.reserved_balance < best_final_price:
                        raise ValidationError(
                            f"Reserved balance ({profile.reserved_balance}) < final price ({best_final_price})"
                        )

                    # 1. Update stock quantity
                    stock.quantity -= 1
                    stock.save(update_fields=["quantity"])

                    # 2. Update autoshow balance (revenue)
                    autoshow.balance += best_final_price
                    autoshow.save(update_fields=["balance"])

                    # 3. Update customer profile balances
                    unused_reserve = offer.max_price - best_final_price
                    profile.reserved_balance -= offer.max_price  # Release entire reserved amount
                    profile.balance += unused_reserve  # Return unused portion to available balance
                    profile.save(update_fields=["reserved_balance", "balance"])

                    # 4. Create sale record
                    Sale.objects.create(
                        autoshow=autoshow,
                        customer=offer.customer,
                        car=offer.car,
                        total_price=best_final_price,
                        price_per_unit=stock.price,
                        discounted_price_per_unit=best_final_price if best_discount else stock.price,
                        discount=best_discount,
                        quantity=1,
                    )

                    # 5. Update offer status
                    offer.status = "COMPLETED"
                    offer.save(update_fields=["status"])

            except Exception as exc:
                print(f"Failed to process offer {offer.id}: {exc}")
                import traceback

                traceback.print_exc()
