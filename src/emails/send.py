from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from .email_service_interface import EmailServiceInterface
from helpers import fields as input_fields
import base64

logger = logging.getLogger('django')


class SendEmailService(EmailServiceInterface):
    def __init__(self):
        self.from_email = getattr(settings, input_fields.DEFAULT_FROM_EMAIL, settings.DEFAULT_FROM_EMAIL)
        self.api_key = getattr(settings, "EMAIL_HOST_PASSWORD", None)
        self.env = getattr(settings, "APP_ENV", "local")

    def send_mail(self, subject: str, recipient_list: list, context: dict, template_name: str, attachments: list = None):
        """
        Automatically routes email sending based on environment.
        """
        if self.env == "production":
            return self._send_via_sendgrid(subject, recipient_list, context, template_name, attachments)
        else:
            return self._send_via_default(subject, recipient_list, context, template_name, attachments)

    def _send_via_sendgrid(self, subject, recipient_list, context, template_name, attachments=None):
        try:
            html_content = render_to_string(template_name, context)
            text_content = strip_tags(html_content)

            for recipient in recipient_list:
                message = Mail(
                    from_email=self.from_email,
                    to_emails=recipient,
                    subject=subject,
                    plain_text_content=text_content,
                    html_content=html_content
                )

                if attachments:
                    for attachment in attachments:
                        with open(attachment[input_fields.PATH], "rb") as f:
                            encoded_file = base64.b64encode(f.read()).decode()
                        message.add_attachment(
                            Attachment(
                                FileContent(encoded_file),
                                FileName(attachment[input_fields.FILENAME]),
                                FileType(attachment[input_fields.MIME_TYPE]),
                                Disposition(input_fields.ATTACHMENT)
                            )
                        )
                sg = SendGridAPIClient(self.api_key)
                sg.send(message)

            logger.info(f"[SendGrid] Email sent successfully to: {recipient_list}")
            return True
        except Exception as e:
            logger.error(f"[SendGrid] Error sending email to {recipient_list}: {e}")
            return False

    def _send_via_default(self, subject, recipient_list, context, template_name, attachments=None):
        try:
            html_content = render_to_string(template_name, context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=recipient_list,
            )
            email.attach_alternative(html_content, input_fields.TEXT_HTML)

            if attachments:
                for attachment in attachments:
                    email.attach_file(attachment[input_fields.PATH], attachment[input_fields.MIME_TYPE])

            email.send(fail_silently=False)
            logger.info(f"[Default SMTP] Email sent successfully to: {recipient_list}")
            return True
        except Exception as e:
            logger.error(f"[Default SMTP] Error sending email to {recipient_list}: {e}")
            return False