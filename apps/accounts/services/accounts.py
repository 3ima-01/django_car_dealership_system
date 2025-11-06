from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from apps.accounts.models import Customers
from apps.accounts.repositories.accounts import AccountsRepository
from apps.accounts.tasks import send_change_email, send_reset_password_email, send_verify_email
from apps.common.utils.jwt import EmailChangeToken, EmailVerificationToken, PasswordResetToken


class AccountsService:
    def __init__(self):
        self.repository = AccountsRepository()

    def register(self, email: str, password: str) -> dict[str, str]:
        customer = Customers.objects.create_user(email=email, password=password)
        token = EmailVerificationToken.for_user(str(customer.id))
        send_verify_email.delay(email, str(token))
        return {"detail": "User successfully register, please verify your email address"}

    def reset_password(self, email: str) -> dict[str, str]:
        customer = self.repository.get_by_email(email)
        if customer:
            token = PasswordResetToken.for_user(str(customer.id))
            send_reset_password_email.delay(email, str(token))
        return {"detail": "Message send to email"}

    def reset_password_confirm(self, token: str, new_password: str) -> dict[str, str]:
        payload = PasswordResetToken(token)
        customer = self.repository.get_by_id(payload["user_id"])
        if customer:
            customer.set_password(new_password)
            customer.save(update_fields=["password"])

        return {"detail": "Password changed successfully"}

    def change_password(self, customer: Customers, old_password: str, new_password: str) -> dict[str, str]:
        if not check_password(old_password, customer.password):
            return {"detail": "Invalid current password"}
        try:
            password_validation.validate_password(new_password, customer)
        except ValidationError as e:
            return {"detail": e.messages}

        customer.set_password(new_password)
        customer.save(update_fields=["password"])

        return {"detail": "Password changed successfully"}

    def change_email(self, customer: Customers, new_email: str) -> dict[str, str]:
        token = EmailChangeToken.for_user(str(customer.id))
        token["new_email"] = new_email
        send_change_email.delay(new_email, str(token))
        return {"detail": "Message send to new email"}

    def change_email_confirm(self, token: str):
        payload = EmailChangeToken(token)
        customer = self.repository.get_by_id(payload["user_id"])
        customer.email = payload["new_email"]
        customer.save(update_fields=["email"])
        return {"detail": "Email change successfully"}

    def verify_email(self, token: str):
        payload = EmailVerificationToken(token)
        self.repository.verify_by_id(payload["user_id"])
        return {"detail": "Email successfully verified"}
