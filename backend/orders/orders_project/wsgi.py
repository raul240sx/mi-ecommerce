import os
from django.core.wsgi import get_wsgi_application

# Docker ya pasa DJANGO_SETTINGS_MODULE como variable de entorno
# Si no existe, usar production por defecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_project.settings.production')

application = get_wsgi_application()