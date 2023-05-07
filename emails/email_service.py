from django.core.mail import send_mail
from django.conf import settings


class EmailService:

    @staticmethod
    def _send(mail_subject: str, message: str, recipient_list: list) -> None:
        email_host = settings.EMAIL_HOST_USER
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=email_host,
            recipient_list=recipient_list
        )

    @staticmethod
    def send_application_response(vacancy_title: str, action: str, message: str, applicant_email: str):
        recipient_list = [applicant_email, ]
        subject = f'{vacancy_title} - {action.capitalize()}'
        EmailService._send(subject, message, recipient_list)
