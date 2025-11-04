from typing import Any

from django.db import transaction

from apps.accounts.dtos.accounts import CustomerRegisterDTO
from apps.accounts.dtos.email import EmailVerifyDTO
from apps.accounts.models import Customers
from apps.accounts.repositories.accounts import AccountsRepository
from apps.accounts.tasks import send_verify_email
from apps.common.utils.jwt import EmailVerificationToken


class AccountsService:
    def __init__(self):
        self.repository = AccountsRepository()

    def register(self, customer_data: CustomerRegisterDTO):
        email = customer_data.email
        password = customer_data.password

        with transaction.atomic():
            customer = Customers(email=email)
            customer.set_password(password)
            customer.save()

            token = EmailVerificationToken()
            token["user_id"] = str(customer.id)
            token = str(token)

            dto = EmailVerifyDTO(
                email=email,
                token=token,
            )

            send_verify_email.delay(dto.model_dump())

            return customer

    def verify_email(self, data: dict[str, Any]):
        token = data.get("token")
        payload = EmailVerificationToken(token)
        self.repository.verify_by_id(payload["user_id"])
