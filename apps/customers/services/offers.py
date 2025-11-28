from decimal import Decimal
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.shortcuts import get_object_or_404

from apps.accounts.models import Customers
from apps.autoshows.models import AutoShows, AutoShowsSales, AutoShowsStock
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
            balance=models.F("balance") + amount,
            reserved_balance=models.F("reserved_balance") - amount,
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
            balance=models.F("balance") - max_price,
            reserved_balance=models.F("reserved_balance") + max_price,
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
        offers = Offers.objects.filter(status="ACTIVE").select_related("customer", "car")

        for offer in offers:
            try:
                with transaction.atomic():
                    # 1.Find stock with minimum price
                    stock = (
                        AutoShowsStock.objects.select_for_update(skip_locked=True)
                        .filter(car=offer.car, quantity__gt=0, price__lte=offer.max_price)
                        .order_by("price", "id")
                        .first()
                    )

                    if not stock:
                        continue

                    # 2.Lock related
                    autoshow = AutoShows.objects.select_for_update().get(id=stock.autoshow_id)
                    profile = Profiles.objects.select_for_update().get(customer=offer.customer)

                    price = stock.price

                    # 3. Check reserverd_balance
                    if profile.reserved_balance < price:
                        raise ValidationError(f"Reserved balance ({profile.reserved_balance}) < price ({price})")

                    # 4. Update Fields
                    # Stock
                    stock.quantity -= 1
                    stock.save(update_fields=["quantity"])

                    # AutoShow
                    autoshow.balance += price
                    autoshow.save(update_fields=["balance"])

                    # Profile
                    unused_reserve = offer.max_price - price
                    profile.reserved_balance -= price + unused_reserve
                    profile.balance += unused_reserve
                    profile.save(update_fields=["reserved_balance", "balance"])

                    # AutoShowsSales
                    AutoShowsSales.objects.create(
                        autoshow=autoshow,
                        customer=offer.customer,
                        car=offer.car,
                        total_price=price,
                    )

                    # Offer
                    offer.status = "COMPLETED"
                    offer.save(update_fields=["status"])

            except Exception as exc:
                print(f"Failed to process offer {offer.id}: {exc}")
