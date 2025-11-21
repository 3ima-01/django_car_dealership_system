from apps.common.utils.email import send_email
from car_dealership_system.celery import app


@app.task(
    bind=True,
    max_retries=5,
)
def send_verify_email(self, email: str, token: str):
    url = f"http://127.0.0.1:8000/api/v1/accounts/verification/?token={token}"

    send_email(
        subject="Verify your email",
        to_emails=[email],
        text_content=f"Your confirmation url: {url}",
    )


@app.task(
    bind=True,
    max_retries=5,
)
def send_reset_password_email(self, email: str, token: str):
    send_email(
        subject="Change your password",
        to_emails=[email],
        text_content=f"Your change password token: {token}",
    )


@app.task(
    bind=True,
    max_retries=5,
)
def send_change_email(self, email: str, token: str):
    url = f"http://127.0.0.1:8000/api/v1/accounts/change-email/confirm/?token={token}"

    send_email(
        subject="Change your email",
        to_emails=[email],
        text_content=f"Your email change url: {url}",
    )
