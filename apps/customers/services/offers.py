from decimal import Decimal
from uuid import UUID

from django.db import models, transaction
from django.shortcuts import get_object_or_404

from apps.accounts.models import Customers
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
        model: str,
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
            model=model,
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

    def get_or_404(self, **kwargs):
        return get_object_or_404(self.model, **kwargs)
