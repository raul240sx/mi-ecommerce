from django.core.mail import EmailMessage, BadHeaderError
from django.template.loader import render_to_string
from django.conf import settings

from smtplib import SMTPException
import logging

logger = logging.getLogger(__name__)


class EmailServiceError(Exception):
    """
    Excepción personalizada para fallos que son temporales y reintentables
    (ej. errores de conexión o SMTP).
    """
    pass


def send_transactional_email(subject:str, email_to:str, template_name:str, context:dict):

    try:
        email_body = render_to_string(template_name, context)
    
    except Exception as e:
        logger.critical(f'Fallo permanente, no se reintentará el envío. Error: {e}')
        raise e
    
    try:
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_to]
            )
        
        email.content_subtype = 'html'

        email.send()

        return True
    
    except (SMTPException, BadHeaderError) as e:
        logger.error(f'[EmailService] Fallo de conexión/SMTP al enviar correo a {email_to} (Plantilla: {template_name}).')
        raise EmailServiceError(f'Fallo de envío de SMTP/Red: {e}')
    
    except Exception as e:
        logger.critical(f'Fallo permanente, no se reintentará el envío. Error: {e}')
        raise e


    