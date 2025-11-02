from typing import Any

from apps.accounts.dtos.accounts import CustomerRegisterDTO
from apps.accounts.dtos.email import EmailVerifyDTO
from apps.accounts.models import Customers
from apps.accounts.repositories.accounts import AccountsRepository
from apps.common.utils.email import send_email
from apps.common.utils.jwt import EmailVerificationToken


class AccountsService:
    def __init__(self):
        self.repository = AccountsRepository()

    def register(self, customer_data: CustomerRegisterDTO):
        email = customer_data.email
        password = customer_data.password

        customer = Customers(email=email)
        customer.set_password(password)
        customer.save()

        token = EmailVerificationToken()
        token["user_id"] = str(customer.id)

        email_verify_dto = EmailVerifyDTO(
            email=email,
            token=str(token),
        )

        self.send_verification_email(email_verify_dto)

        return customer

    def verify_email(self, data: dict[str, Any]):
        token = data.get("token")
        payload = EmailVerificationToken(token)
        self.repository.verify_by_id(payload["user_id"])

    def send_verification_email(self, email_verify_dto: EmailVerifyDTO):
        verify_url = f"http://127.0.0.1:8000/api/v1/accounts/verify-email/?token={email_verify_dto.token}"

        send_email(
            subject="Подтвердите ваш email",
            to_emails=[email_verify_dto.email],
            text_content=f"Перейдите по ссылке для подтверждения: {verify_url}",
        )
