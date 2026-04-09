# GuitarZone - Guía de Desarrollo y Deployment

Instrucciones completas para desarrollar localmente, deployar a producción y mantener el proyecto.

## 📋 Tabla de Contenidos

1. [Setup Inicial de Desarrollo](#setup-inicial-de-desarrollo)
2. [Flujo de Desarrollo](#flujo-de-desarrollo)
3. [Testing](#testing)
4. [Deployment a Producción](#deployment-a-producción)
5. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
6. [Troubleshooting](#troubleshooting)
7. [Comandos Útiles](#comandos-útiles)

---

## 🚀 Setup Inicial de Desarrollo

### Requisitos Previos

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Git** 2.30+
- **Python** 3.10+ (para desarrollo local sin Docker)
- **Visual Studio Code** (recomendado)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/raul240sx/guitarzone-backend.git
cd guitarzone-backend

# Crear rama de desarrollo
git checkout -b develop
```

### Paso 2: Configurar Variables de Entorno

**Archivo .env en raíz:**
```bash
cp .env.example .env

# Editar .env
POSTGRES_USER=guitarzone_user
POSTGRES_PASSWORD=guitarzone_dev_pass
```

**Archivo backend/users/.env:**
```bash
cp backend/users/.env.example backend/users/.env

# Contenido recomendado para desarrollo:
SECRET_KEY=django-insecure-5x%7b3f3c6k9p2l5m8n1q4r7t0v3w6x9z2c5f8i1l4o7r0t3w
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,users-service

DATABASE_URL=postgresql://guitarzone_user:guitarzone_dev_pass@users-db:5432/users_db

JWT_SECRET_KEY=jwt-secret-dev-key-change-in-production
RSA_PUBLIC_KEY_PATH=/run/secrets/rsa_public_key.pem
RSA_PRIVATE_KEY_PATH=/run/secrets/rsa_private_key.pem

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
SITE_NAME=GuitarZone
SITE_URL=http://localhost:3000
VERIFY_URL_PATH=verify-email

REDIS_URL=redis://redis-service:6379/0

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

PRODUCTS_SERVICE_URL=http://products-service:8000
ORDERS_SERVICE_URL=http://orders-service:8000
INTERNAL_SERVICE_KEY=dev-internal-key-change-in-production
```

**Archivo backend/products/.env:**
```bash
SECRET_KEY=django-insecure-5x%7b3f3c6k9p2l5m8n1q4r7t0v3w6x9z2c5f8i1l4o7r0t3w
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,products-service

DATABASE_URL=postgresql://guitarzone_user:guitarzone_dev_pass@products-db:5432/products_db

JWT_SECRET_KEY=jwt-secret-dev-key-change-in-production
RSA_PUBLIC_KEY_PATH=/run/secrets/rsa_public_key.pem

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

INTERNAL_SERVICE_KEY=dev-internal-key-change-in-production
```

**Archivo backend/orders/.env:**
```bash
SECRET_KEY=django-insecure-5x%7b3f3c6k9p2l5m8n1q4r7t0v3w6x9z2c5f8i1l4o7r0t3w
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,orders-service

DATABASE_URL=postgresql://guitarzone_user:guitarzone_dev_pass@orders-db:5432/orders_db

JWT_SECRET_KEY=jwt-secret-dev-key-change-in-production
RSA_PUBLIC_KEY_PATH=/run/secrets/rsa_public_key.pem

MERCADOPAGO_ACCESS_TOKEN=APP_USR_TEST_TOKEN_HERE
FRONTEND_URL=http://localhost:3000

REDIS_URL=redis://redis-service:6379/0

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

PRODUCTS_SERVICE_URL=http://products-service:8000
PRODUCTS_RESERVE_STOCK=http://products-service:8000/products-api/reserve-stock/
PRODUCTS_RELEASE_STOCK=http://products-service:8000/products-api/release-stock/
INTERNAL_SERVICE_KEY=dev-internal-key-change-in-production
```

### Paso 3: Generar Claves RSA

```bash
# En la raíz del proyecto
mkdir -p secrets/users secrets/products secrets/orders

# Generar clave privada (2048 bits)
openssl genrsa -out rsa_private_key.pem 2048

# Generar clave pública
openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem

# Copiar claves
cp rsa_private_key.pem secrets/users/
cp rsa_public_key.pem secrets/users/
cp rsa_public_key.pem secrets/products/
cp rsa_public_key.pem secrets/orders/

# Verificar permisos
chmod 400 secrets/users/rsa_private_key.pem
chmod 444 secrets/*/*.pem
```

### Paso 4: Levantar Contenedores

```bash
# Build de imágenes
docker-compose build

# Levantar servicios
docker-compose up -d

# Verificar que todo esté running
docker-compose ps

# Ver logs
docker-compose logs -f
```

**Esperado:**
```
✓ users-db        (postgres)
✓ products-db     (postgres)
✓ orders-db       (postgres)
✓ redis-service   (redis)
✓ users-service   (django)
✓ products-service (django)
✓ orders-service  (django)
✓ users-celery    (celery worker)
✓ orders-celery   (celery worker)
```

### Paso 5: Ejecutar Migraciones

```bash
# Users Service
docker-compose exec users-service python manage.py migrate

# Products Service
docker-compose exec products-service python manage.py migrate

# Orders Service
docker-compose exec orders-service python manage.py migrate
```

### Paso 6: Crear Superusuario

```bash
docker-compose exec users-service python manage.py createsuperuser

# Ingresar:
# Email: admin@guitarzone.local
# Password: AdminPass123!
```

### Paso 7: Cargar Datos Iniciales (Opcional)

```bash
# Cargar regiones y comunas de Chile
docker-compose exec users-service python manage.py loaddata regions_communes

# Cargar categorías de productos
docker-compose exec products-service python manage.py loaddata product_categories

# Cargar unidades de medida
docker-compose exec products-service python manage.py loaddata measure_units
```

### Paso 8: Verificar Funcionamiento

```bash
# Users Service
curl http://localhost:7000/api/schema/swagger/

# Products Service
curl http://localhost:7100/api/schema/swagger/

# Orders Service
curl http://localhost:7200/api/schema/swagger/
```

Accede a:
- Users Swagger: `http://localhost:7000/api/schema/swagger/`
- Products Swagger: `http://localhost:7100/api/schema/swagger/`
- Orders Swagger: `http://localhost:7200/api/schema/swagger/`
- Admin (Users): `http://localhost:7000/admin/`

---

## 🔄 Flujo de Desarrollo

### Crear Nueva Funcionalidad

```bash
# 1. Crear rama de feature
git checkout -b feature/nueva-funcionalidad

# 2. Hacer cambios en el código

# 3. Verificar que Docker está actualizado
docker-compose restart <servicio>

# Los archivos están mapeados por volumen, auto-reload

# 4. Ejecutar tests
docker-compose exec <servicio> python manage.py test

# 5. Crear migraciones si cambió models
docker-compose exec <servicio> python manage.py makemigrations

# 6. Ejecutar migraciones
docker-compose exec <servicio> python manage.py migrate

# 7. Commit
git add .
git commit -m "feat: descripción de cambios"

# 8. Push a rama feature
git push origin feature/nueva-funcionalidad

# 9. Crear Pull Request
```

### Estructura de Commits

```
feat: agregar nueva funcionalidad
fix: corregir bug específico
refactor: cambios en código sin alterar funcionalidad
docs: cambios solo en documentación
test: agregar o actualizar tests
chore: cambios en build/dependencies
ci: cambios en CI/CD
```

### Desarrollo Local sin Docker

**Para desarrollar sin Docker localmente:**

```bash
# Users Service
cd backend/users

# Crear venv
python3 -m venv venv_users
source venv_users/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# crear .env
touch .env

# Ejecutar servidor
python manage.py runserver 8000
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
docker-compose exec users-service python manage.py test

# Tests específicos de app
docker-compose exec users-service python manage.py test apps.users

# Tests específicos de una clase
docker-compose exec users-service python manage.py test apps.users.tests.TestUserRegistration

# Con coverage
docker-compose exec users-service coverage run --source='.' manage.py test
docker-compose exec users-service coverage report
```

### Ejemplo de Test

```python
# backend/users/apps/users/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/users-api/auth/register/'
    
    def test_user_registration_success(self):
        """Test registro exitoso de usuario"""
        data = {
            'email': 'newuser@guitarzone.com',
            'password': 'TestPass123!',
            'first_name': 'Juan',
            'last_name': 'Pérez'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data['email']).exists())
    
    def test_user_registration_duplicate_email(self):
        """Test que email duplicado falla"""
        email = 'test@guitarzone.com'
        User.objects.create_user(email=email, password='Pass123!')
        
        data = {
            'email': email,
            'password': 'TestPass123!',
            'first_name': 'Juan',
            'last_name': 'Pérez'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

---

## 🚀 Deployment a Producción

### Pre-requisitos Producción

- **Servidor Linux** (Ubuntu 22.04 LTS recomendado)
- **Docker & Docker Compose**
- **Domain name** (guitarzone.cl)
- **SSH access** al servidor
- **SSL Certificate** (Let's Encrypt gratuito)
- **Mercado Pago account** con credenciales reales
- **SMTP server** para envío de emails

### Paso 1: Preparar Servidor

```bash
# SSH al servidor
ssh root@api.guitarzone.cl

# Actualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt install docker-compose -y

# Verificar instalación
docker --version
docker-compose --version
```

### Paso 2: Clonar Repositorio

```bash
# En el servidor
cd /opt
git clone https://github.com/raul240sx/guitarzone-backend.git
cd guitarzone-backend

# Cambiar a rama stable
git checkout main  # o produccion-estable
```

### Paso 3: Configurar Producción

**Crear .env con valores reales:**

```bash
# /opt/guitarzone-backend/.env
POSTGRES_USER=guitarzone_prod_user
POSTGRES_PASSWORD=CONTRASEÑA_SUPER_SEGURA_AQUI_MIN_32_CARACTERES
POSTGRES_SECURE_PASSWORD=OTRA_CONTRASEÑA_MUY_FUERTE_AQUI
```

**backend/users/.env (Producción):**

```bash
SECRET_KEY=GENERAR_UNA_NUEVA_EN_djecrety.ir
DEBUG=False
ALLOWED_HOSTS=api.guitarzone.cl
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

DATABASE_URL=postgresql://guitarzone_prod_user:CONTRASEÑA@users-db:5432/users_db

JWT_SECRET_KEY=GENERAR_NUEVA_CLAVE_AQUI
RSA_PUBLIC_KEY_PATH=/run/secrets/rsa_public_key.pem
RSA_PRIVATE_KEY_PATH=/run/secrets/rsa_private_key.pem

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=guitarzone.noreply@gmail.com
EMAIL_HOST_PASSWORD=APP_PASSWORD_GENERATED_IN_GMAIL
SITE_NAME=GuitarZone
SITE_URL=https://guitarzone.cl
VERIFY_URL_PATH=verify-email

REDIS_URL=redis://redis-service:6379/0

CORS_ALLOWED_ORIGINS=https://guitarzone.cl,https://www.guitarzone.cl

PRODUCTS_SERVICE_URL=http://products-service:8000
ORDERS_SERVICE_URL=http://orders-service:8000
INTERNAL_SERVICE_KEY=GENERAR_CLAVE_MUY_SEGURA_AQUI

LOG_LEVEL=INFO
SENTRY_DSN=https://...(opcional para error tracking)
```

**Copiar similarly para products y orders .env**

### Paso 4: Generar Claves RSA y SSL

```bash
# RSA Keys
cd /opt/guitarzone-backend
mkdir -p secrets/users secrets/products secrets/orders

openssl genrsa -out rsa_private_key.pem 2048
openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem

cp rsa_private_key.pem secrets/users/
cp rsa_public_key.pem secrets/users/
cp rsa_public_key.pem secrets/products/
cp rsa_public_key.pem secrets/orders/

chmod 400 secrets/users/rsa_private_key.pem
chmod 444 secrets/*/*.pem

# SSL Connection con Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y

sudo certbot certonly --standalone -d api.guitarzone.cl \
  -d guitarzone.cl -d www.guitarzone.cl

# Certificados en: /etc/letsencrypt/live/api.guitarzone.cl/
```

### Paso 5: Build y Deploy

```bash
cd /opt/guitarzone-backend

# Build con docker-compose-prod.yml
docker-compose -f docker-compose-prod.yml build

# Levantar servicios en background
docker-compose -f docker-compose-prod.yml up -d

# Verificar status
docker-compose -f docker-compose-prod.yml ps

# Ejecutar migraciones
docker-compose -f docker-compose-prod.yml exec users-service \
  python manage.py migrate

docker-compose -f docker-compose-prod.yml exec products-service \
  python manage.py migrate

docker-compose -f docker-compose-prod.yml exec orders-service \
  python manage.py migrate

# Crear superusuario
docker-compose -f docker-compose-prod.yml exec users-service \
  python manage.py createsuperuser

# Cargar datos iniciales
docker-compose -f docker-compose-prod.yml exec users-service \
  python manage.py loaddata regions_communes
```

### Paso 6: Configurar Nginx SSL

**Actualizar nginx/default.conf:**

```nginx
# Redirigir HTTP a HTTPS
server {
    listen 80;
    server_name api.guitarzone.cl guitarzone.cl www.guitarzone.cl;
    return 301 https://$server_name$request_uri;
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name api.guitarzone.cl;
    
    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/api.guitarzone.cl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.guitarzone.cl/privkey.pem;
    
    # SSL Optimization
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # ... resto de configuración
}
```

### Paso 7: Health Checks

```bash
# Verificar que servicios están up
curl -s http://localhost:7000/api/health/ | jq .

# Verificar DB connectivity
docker-compose -f docker-compose-prod.yml exec users-db \
  psql -U guitarzone_prod_user -d users_db -c "SELECT 1;"

# Revisar logs
docker-compose -f docker-compose-prod.yml logs -f nginx
docker-compose -f docker-compose-prod.yml logs -f users-service
```

---

## 📊 Monitoreo y Mantenimiento

### Logs y Debugging

```bash
# Ver logs en tiempo real
docker-compose -f docker-compose-prod.yml logs -f

# Logs de servicio específico
docker-compose -f docker-compose-prod.yml logs -f users-service

# Últimas 100 líneas
docker-compose -f docker-compose-prod.yml logs --tail=100 users-service

# Exportar logs
docker-compose -f docker-compose-prod.yml logs > logs_backup.txt
```

### Monitoreo de Performance

```bash
# Revisar uso de recursos
docker stats

# Revisar procesos en DB
docker-compose -f docker-compose-prod.yml exec users-db \
  psql -U guitarzone_prod_user -d users_db -c \
  "SELECT * FROM pg_stat_activity WHERE state = 'active';"

# Revisar tamaño de BD
docker-compose -f docker-compose-prod.yml exec users-db \
  psql -U guitarzone_prod_user -d users_db -c \
  "SELECT pg_size_pretty(pg_database_size('users_db'));"
```

### Backups

```bash
# Backup de Users DB
docker-compose -f docker-compose-prod.yml exec users-db \
  pg_dump -U guitarzone_prod_user users_db > users_db_backup_$(date +%Y%m%d).sql

# Backup de Products DB
docker-compose -f docker-compose-prod.yml exec products-db \
  pg_dump -U guitarzone_prod_user products_db > products_db_backup_$(date +%Y%m%d).sql

# Backup de Orders DB
docker-compose -f docker-compose-prod.yml exec orders-db \
  pg_dump -U guitarzone_prod_user orders_db > orders_db_backup_$(date +%Y%m%d).sql

# Restaurar desde backup
cat users_db_backup_FECHA.sql | \
  docker-compose -f docker-compose-prod.yml exec -T users-db \
  psql -U guitarzone_prod_user users_db
```

### Limpieza de Datos

```bash
# Limpiar archivos temporales
docker-compose exec users-service python manage.py cleanuptoken

# Limpiar sesiones expiradas
docker-compose exec users-service python manage.py clearsessions

# Limpiar caché
docker-compose exec redis-service redis-cli FLUSHALL
```

### Updates y Patches

```bash
# Traer cambios del repo
cd /opt/guitarzone-backend
git pull origin main

# Rebuild imágenes
docker-compose -f docker-compose-prod.yml build

# Recrear contenedores (zero downtime para Django)
docker-compose -f docker-compose-prod.yml up -d

# Ejecutar migraciones si las hay
docker-compose -f docker-compose-prod.yml exec users-service \
  python manage.py migrate
```

---

## 🔧 Troubleshooting

### Problema: Conexión rechazada a DB

```bash
# Verificar que containers están running
docker-compose ps

# Revisar logs de DB
docker-compose logs users-db

# Conectar manualmente a DB
docker-compose exec users-db psql -U guitarzone_user -d users_db

# Verificar variables de entorno
docker-compose exec users-service env | grep DATABASE_URL
```

### Problema: Email no se envía

```bash
# Para desarrollo, emails van a console
# Ver logs
docker-compose logs users-service | grep "Subject:"

# Para producción, verificar SMTP
docker-compose exec users-service python manage.py test apps.users.tests.TestEmailSending

# Verificar credenciales en .env
docker-compose exec users-service python manage.py shell
>>> from django.conf import settings
>>> print(settings.EMAIL_HOST_USER, settings.EMAIL_HOST)
```

### Problema: Stock no se libera

```bash
# Ver tasks en Celery
docker-compose logs users-celery | grep "release_stock_task"

# Verificar Redis connection
docker-compose exec redis-service redis-cli PING

# Revisar queue de tasks
docker-compose exec redis-service redis-cli KEYS "celery*"

# Ejecutar task manualmente (testing)
docker-compose exec orders-service python manage.py shell
>>> from apps.orders.tasks import release_stock_task
>>> release_stock_task(order_id=1)
```

### Problema: JWT Token inválido

```bash
# Verificar claves RSA existen y son correctas
ls -la secrets/*/rsa_*.pem

# Verificar contenido de clave pública (debe tener BEGIN/END)
cat secrets/users/rsa_public_key.pem

# Regenerar claves si es necesario
cd secrets && rm -f */rsa_*.pem
openssl genrsa -out rsa_private_key.pem 2048
...
```

### Problema: CORS errors

```bash
# Verificar configuración de CORS en .env
echo $CORS_ALLOWED_ORIGINS

# Verificar headers de response
curl -i -X OPTIONS http://localhost:7000/users-api/ \
  -H "Origin: http://localhost:3000"
```

---

## 📝 Comandos Útiles

```bash
# SSH al contenedor
docker-compose exec <servicio> bash

# Django shell
docker-compose exec users-service python manage.py shell

# Crear usuario desde shell
docker-compose exec users-service python manage.py shell <<EOF
from apps.users.models import User
User.objects.create_superuser('admin@guitarzone.com', 'password123')
EOF

# Resetear migraciones (⚠️ CUIDADO: borra datos)
docker-compose exec <servicio> python manage.py migrate <app> zero

# Ejecutar comando personalizado
docker-compose exec users-service python manage.py custom_command

# Ver todas las migraciones
docker-compose exec users-service python manage.py showmigrations

# Collectstatic (archivos estáticos)
docker-compose exec users-service python manage.py collectstatic --noinput

# Limpiar pycache
docker-compose exec users-service find . -type d -name __pycache__ -exec rm -rf {} +

# Format código con black
docker-compose exec users-service black apps/

# Lint con flake8
docker-compose exec users-service flake8 apps/ --max-line-length=120

# Restart servicios
docker-compose restart users-service products-service orders-service

# Watch logs específicos
docker-compose logs -f --tail=50 orders-celery

# Rebuild sin cache
docker-compose build --no-cache

# Parar todos sin eliminar volumes
docker-compose down

# Parar y eliminar todo (⚠️)
docker-compose down -v
```

---

## 📚 Referencias Útiles

- [Docker Compose CLI Reference](https://docs.docker.com/compose/reference/)
- [Django Management Commands](https://docs.docker.com/compose/reference/)
- [Celery Tasks](https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html)
- [PostgreSQL Administration](https://www.postgresql.org/docs/15/admin.html)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt Certificate](https://letsencrypt.org/getting-started/)

---

**Última actualización:** Abril 2026
