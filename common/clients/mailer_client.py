from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class MailerClient:
    def __init__(self):
        pass

    def send_email(
        self,
        email_template: str,
        subject: str,
        message: str,
        to: str,
        sender_name: str
    ):
        email_body = render_to_string(email_template, {
            'subject': subject,
            'message': message,
        })

        email = EmailMessage(subject, email_body, from_email=sender_name, to=[to])
        email.content_subtype = "html"
        email.send()
