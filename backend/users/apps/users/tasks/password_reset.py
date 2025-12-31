import logging
from celery import shared_task
from celery.exceptions import Retry, MaxRetriesExceededError

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


from apps.users.models.user import User
from apps.users.services.email_service import send_transactional_email, EmailServiceError


logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, acks_late=True, name='password_reset_task')
def password_reset_task(self, user_id):
    try:
        user = User.objects.get(id=user_id)
    
    except User.DoesNotExist:
        logger.warning(f"[PasswordReset] Usuario no encontrado: user_id={user_id}")
        return

    try:
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        subject = f'Reset de contraseña {settings.SITE_NAME}'
        email_to = user.email
        template_name = 'emails/password_reset_email.html'
        reset_link = f'{settings.SITE_URL}/{settings.RESET_URL_PATH}?uidb64={uidb64}&token={token}'

        context = {
            'user':user,
            'reset_link': reset_link,
            'site_name': settings.SITE_NAME,
        }


        send_transactional_email(subject=subject, email_to=email_to, template_name=template_name, context=context)
        

        
    except EmailServiceError as e:
        logger.error(f'[EmailService] No se ha podido enviar el email al user_id={user_id}. Reintentando', exc_info=True)
        try:
            raise self.retry(exc=e)
    
        except MaxRetriesExceededError:
            logger.critical(f'[PasswordReset] Fallo permanente después de {self.max_retries} intentos. UserID: {user_id}.')
            return



