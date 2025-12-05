from datetime import timedelta
from typing import Self

from rest_framework_simplejwt.tokens import Token

from car_dealership_system.settings.config import config


class BaseToken(Token):
    @classmethod
    def for_user(cls, id: str) -> Self:
        token = cls()
        token["user_id"] = id
        return token


class EmailVerificationToken(BaseToken):
    token_type = "email_verification"
    lifetime = timedelta(hours=config.jwt.EMAIL_VERIFY_TOKEN_LIFETIME)


class PasswordResetToken(BaseToken):
    token_type = "reset_password"
    lifetime = timedelta(minutes=config.jwt.ACTION_TOKEN_LIFETIME)


class EmailChangeToken(BaseToken):
    token_type = "email_change"
    lifetime = timedelta(minutes=config.jwt.ACTION_TOKEN_LIFETIME)
