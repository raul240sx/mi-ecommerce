#!/bin/sh
set -e

mkdir -p /usr/src/app/media /usr/src/app/staticfiles /tmp/gunicorn
chown -R appuser:appuser /usr/src/app/media /usr/src/app/staticfiles /tmp/gunicorn

if [ "$DEBUG" = "False" ] || [ "$DEBUG" = "false" ]; then
    echo "--- MODO PRODUCCIÓN DETECTADO ---"
    
    gosu appuser python manage.py migrate --noinput
    gosu appuser python manage.py collectstatic --noinput

    echo "Arrancando con GUNICORN (Producción)..."
    exec gosu appuser gunicorn ${DJANGO_PROJECT_NAME}.wsgi:application \
        --bind 0.0.0.0:8000 \
        --worker-tmp-dir /tmp/gunicorn

else
    echo "--- MODO DESARROLLO (LOCAL) DETECTADO ---"
fi

echo "Ejecutando: $*"
exec gosu appuser "$@"