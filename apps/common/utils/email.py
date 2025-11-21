from typing import List, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(
    subject: str,
    to_emails: List[str],
    text_content: Optional[str] = None,
    html_content: Optional[str] = None,
    from_email: Optional[str] = None,
):
    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content or "",
        from_email=from_email,
        to=to_emails,
    )

    if html_content:
        msg.attach_alternative(html_content, "text/html")

    return msg.send()


def send_email_from_template(
    subject: str,
    to_emails: List[str],
    template_name: str,
    context: dict,
    from_email: Optional[str] = None,
):
    html_content = render_to_string(template_name, context)
    text_content = render_to_string(template_name.replace(".html", ".txt"), context)

    return send_email(
        subject=subject,
        to_emails=to_emails,
        text_content=text_content,
        html_content=html_content,
        from_email=from_email,
    )
