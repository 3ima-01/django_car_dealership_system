from datetime import timedelta

from rest_framework_simplejwt.tokens import Token


class EmailVerificationToken(Token):
    token_type = "email_verification"
    lifetime = timedelta(hours=6)
