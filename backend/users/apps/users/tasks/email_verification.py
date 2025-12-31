from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

import logging
from celery import shared_task
from celery.exceptions import Retry, MaxRetriesExceededError


from apps.users.models.user import User
from apps.users.tokens.email_verification import EmailVerificationTokenGenerator
from apps.users.services.email_service import send_transactional_email, EmailServiceError



logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, acks_late=True, name='send_verification_email_task')
def send_verification_email_task(self, user_id):

    try:
        user = User.objects.get(id=user_id)

    except User.DoesNotExist:
        logger.warning(f"[VerificationEmail] Usuario no encontrado: user_id={user_id}.")
        return
    
    if user.is_verified:
        logger.warning(f"[VerificationEmail] Usuario ya se encuentra verificado. Se omitirá la verificacion por email.")
        return
    



    try:
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = EmailVerificationTokenGenerator().make_token(user)

        subject = f'Verificación de cuenta {settings.SITE_NAME}'
        email_to = user.email
        template_name = 'emails/verification_email.html'
        verify_link = f'{settings.SITE_URL}/{settings.VERIFY_URL_PATH}?uidb64={uidb64}&token={token}'

        #'verify_link': verify_link,  ### Por pruebas voy a poner la ip de mi server con su endpoint de react router

        context = {
            'username':user.email.split('@')[0],
            'verify_link': f'http://192.168.1.201:5173/email-verification?uidb64={uidb64}&token={token}',
            'site_name': settings.SITE_NAME,
        }

        send_transactional_email(subject=subject, email_to=email_to, template_name=template_name, context=context)

    except EmailServiceError as e:
        logger.error(f'[VerificationEmail] Fallo temporal al enviar email a {user.email}. Reintentando...', exc_info=True)
        try:
            raise self.retry(exc=e)
        except MaxRetriesExceededError:
            logger.critical(f'[VerificationEmail] Fallo permanente para {user.email} después de {self.max_retries} intentos.')
            return

    except Exception as e: 
        logger.critical(f'[VerificationEmail] Fallo de código inesperado y no reintentable para {user.email}. Detalle: {e}', exc_info=True)
        return

