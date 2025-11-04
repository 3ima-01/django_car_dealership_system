from apps.accounts.dtos.email import EmailVerifyDTO
from apps.common.utils.email import send_email
from car_dealership_system.celery import app


@app.task(
    bind=True,
    max_retries=5,
)
def send_verify_email(self, data: dict[str, str]):
    dto = EmailVerifyDTO(**data)

    verify_url = f"http://127.0.0.1:8000/api/v1/accounts/verify-email/?token={dto.token}"

    send_email(
        subject="Подтвердите ваш email",
        to_emails=[dto.email],
        text_content=f"Перейдите по ссылке для подтверждения: {verify_url}",
    )
