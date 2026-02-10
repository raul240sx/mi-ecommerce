#!/bin/sh
set -e

# 1. Preparación de carpetas (Siempre necesaria por permisos)
mkdir -p /usr/src/app/media /usr/src/app/staticfiles
chown -R appuser:appuser /usr/src/app/media /usr/src/app/staticfiles

# 2. Lógica condicional basada en DEBUG
# Nota: Como cargamos .env en base.py, aquí la leemos directamente del sistema
if [ "$DEBUG" = "False" ] || [ "$DEBUG" = "false" ]; then
    echo "--- MODO PRODUCCIÓN DETECTADO ---"
    
    echo "Aplicando migraciones..."
    su -s /bin/sh appuser -c "python manage.py migrate --noinput"

    echo "Recopilando archivos estáticos..."
    su -s /bin/sh appuser -c "python manage.py collectstatic --noinput"

    echo "Arrancando con GUNICORN (Producción)..."
    # Ejecutamos gunicorn ignorando lo que diga el CMD del Dockerfile
    exec su -s /bin/sh appuser -c "gunicorn ${DJANGO_PROJECT_NAME}.wsgi:application --bind 0.0.0.0:8000"

else
    echo "--- MODO DESARROLLO (LOCAL) DETECTADO ---"
fi

# 3. Ejecutar el comando final (runserver o gunicorn)
echo "Ejecutando: $*"
exec su -s /bin/sh appuser -c "$*"