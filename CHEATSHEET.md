# GuitarZone - Quick Reference (CheatSheet)

Referencia rápida de comandos, endpoints y soluciones comunes.

---

## 🚀 Quick Start

```bash
# Setup inicial
git clone https://github.com/raul240sx/guitarzone-backend.git
cd guitarzone-backend

# Generar claves RSA
openssl genrsa -out rsa_private_key.pem 2048
openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem
mkdir -p secrets/users secrets/products secrets/orders
cp rsa_private_key.pem secrets/users/ && cp rsa_public_key.pem secrets/{users,products,orders}/

# Levantar
docker-compose up --build -d

# Migraciones
docker-compose exec -T users-service python manage.py migrate
docker-compose exec -T products-service python manage.py migrate
docker-compose exec -T orders-service python manage.py migrate

# Superuser
docker-compose exec users-service python manage.py createsuperuser
```

---

## 📍 Endpoints Principales

### Users Service (http://localhost:7000 o /users-api/)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register/` | Registrar usuario |
| POST | `/auth/login/` | Login (retorna access + refresh token) |
| POST | `/auth/verify-email/` | Verificar email |
| GET | `/users/me/` | Datos del usuario |
| PATCH | `/users/me/` | Actualizar perfil |
| POST | `/auth/password-reset/` | Reset contraseña |
| POST | `/auth/change-password/` | Cambiar contraseña |
| POST | `/addresses/` | Crear dirección |
| GET | `/addresses/` | Listar direcciones |
| PATCH | `/addresses/{id}/` | Actualizar dirección |
| DELETE | `/addresses/{id}/` | Eliminar dirección |
| GET | `/locations/regions/` | Listar regiones |
| GET | `/locations/communes/` | Listar comunas |

### Products Service (http://localhost:7100 o /products-api/)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/products/` | Listar productos (público) |
| GET | `/products/{id}/` | Detalle producto |
| POST | `/products/` | Crear producto (staff) |
| PATCH | `/products/{id}/` | Editar producto (staff) |
| DELETE | `/products/{id}/` | Eliminar producto (staff) |
| GET | `/categories/` | Listar categorías |
| POST | `/categories/` | Crear categoría (staff) |
| GET | `/measure-units/` | Listar unidades |
| POST | `/measure-units/` | Crear unidad (staff) |
| POST | `/reserve-stock/` | Reservar stock (interno) |
| POST | `/release-stock/` | Liberar stock (interno) |

### Orders Service (http://localhost:7200 o /orders-api/)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/orders/` | Crear orden |
| GET | `/orders/` | Listar órdenes del usuario |
| GET | `/orders/{id}/` | Detalle de orden |
| PATCH | `/orders/{id}/update-address/` | Actualizar dirección envío |
| GET | `/payment/preference/{order_id}/` | Obtener link de pago MP |
| POST | `/webhook/` | Webhook de Mercado Pago |

---

## 🔑 Headers Comunes

```bash
# Autenticación
Authorization: Bearer <access_token>

# Interno (entre servicios)
X-Internal-Service-Key: <internal_key>

# Para webhook de MP
X-Signature: <signature_from_mp>
```

---

## 🔐 Autenticación

### Registro
```bash
curl -X POST http://localhost:7000/users-api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@guitarzone.com",
    "password": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

### Login
```bash
curl -X POST http://localhost:7000/users-api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@guitarzone.com",
    "password": "SecurePass123!"
  }'

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar Token
```bash
curl -X GET http://localhost:7000/users-api/users/me/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 🛒 Carrito y Orden

### Listar Productos
```bash
# Todos
curl http://localhost:7100/products-api/products/

# Filtrado
curl "http://localhost:7100/products-api/products/?category=1&min_price=50000&max_price=300000&search=guitarra"

# Paginación
curl "http://localhost:7100/products-api/products/?page=2&page_size=10"
```

### Crear Orden
```bash
curl -X POST http://localhost:7200/orders-api/orders/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "order_items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 3, "quantity": 1}
    ]
  }'

# Response:
{
  "message": "Orden creada correctamente",
  "order": {
    "id": 123,
    "user_id": 5,
    "status": "PENDING",
    "total_amount": 450000,
    "order_items": [...]
  }
}
```

### Iniciar Pago (Mercado Pago)
```bash
curl -X GET http://localhost:7200/orders-api/payment/preference/123/ \
  -H "Authorization: Bearer <access_token>"

# Response:
{
  "init_point": "https://www.mercadopago.com/checkout/v1/..."
}

# Usuario es redirigido a init_point para pagar
```

---

## 📦 Consultas Frecuentes (SQL)

### Registrar Actividad de Usuario
```sql
-- Users DB
SELECT * FROM simple_history_historicaluser 
ORDER BY history_date DESC LIMIT 10;

-- Órdenes del usuario
SELECT * FROM orders_order WHERE user_id = 5;
```

### Productos Bajo Stock
```sql
-- Products DB
SELECT id, name, stock FROM products_product 
WHERE stock < 5 AND state = true;
```

### Órdenes Pendientes de Pago
```sql
-- Orders DB
SELECT * FROM orders_order 
WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL '30 minutes';
```

### Historial de Cambios
```sql
-- Qué cambió en un producto
SELECT * FROM simple_history_historicalproduct 
WHERE id = 1 
ORDER BY history_date DESC;
```

---

## 🔧 Comandos Docker Frecuentes

```bash
# Ver estado
docker-compose ps

# Logs
docker-compose logs -f
docker-compose logs users-service
docker-compose logs --tail=50 orders-celery

# Conectar a contenedor
docker-compose exec users-service bash
docker-compose exec users-db psql -U guitarzone_user -d users_db

# Restart
docker-compose restart
docker-compose restart users-service

# Stop/Up
docker-compose down
docker-compose up -d

# Build sin cache
docker-compose build --no-cache

# Ver recursos
docker stats
```

---

## 🐍 Django Commands

```bash
# Migraciones
docker-compose exec users-service python manage.py makemigrations
docker-compose exec users-service python manage.py migrate
docker-compose exec users-service python manage.py migrate --fake-initial

# Admin
docker-compose exec users-service python manage.py createsuperuser
docker-compose exec users-service python manage.py changepassword admin

# Data
docker-compose exec users-service python manage.py loaddata regions_communes
docker-compose exec users-service python manage.py dumpdata > data.json

# Testing
docker-compose exec users-service python manage.py test
docker-compose exec users-service python manage.py test apps.users

# Shell
docker-compose exec users-service python manage.py shell

# Lint
docker-compose exec users-service python -m black apps/
docker-compose exec users-service python -m flake8 apps/
```

---

## 🛠️ Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| **DB no conecta** | `docker-compose logs users-db` + verificar .env |
| **Migraciones fallan** | `docker-compose exec users-service python manage.py migrate --fake-initial` |
| **Email no funciona** | Verificar SMTP en .env, para dev use console backend |
| **Stock no se libera** | Verificar `docker-compose logs users-celery` + redis running |
| **JWT token inválido** | Regenerar claves RSA + reiniciar servicios |
| **CORS errors** | Verificar CORS_ALLOWED_ORIGINS en .env |
| **Port ya en uso** | `lsof -i :7000` + cambiar puerto en docker-compose.yml |
| **Contenedor crash** | `docker-compose logs <servicio>` para ver error |
| **Redis no responde** | `docker-compose exec redis-service redis-cli PING` |
| **Mercado Pago falla** | Verificar ACCESS_TOKEN en .env (usar TEST token para dev) |

---

## 📊 Monitoreo Rápido

```bash
# Verificar salud general
docker-compose exec users-service python manage.py runserver 0.0.0.0:8001

# Conexión a bases de datos
docker-compose exec users-db psql -U guitarzone_user -d users_db -c "SELECT 1;"

# Performance de DB
docker-compose exec users-db psql -U guitarzone_user -d users_db -c \
  "SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 5;"

# Tamaño de BD
docker-compose exec users-db psql -U guitarzone_user -d users_db -c \
  "SELECT pg_size_pretty(pg_database_size('users_db'));"

# Tasks en Celery
docker-compose exec redis-service redis-cli KEYS "*"
docker-compose exec redis-service redis-cli LLEN celery

# Conexiones activas
docker-compose exec users-db psql -U guitarzone_user -d users_db -c \
  "SELECT usename, state FROM pg_stat_activity;"
```

---

## 🔄 Deploying a Producción (Rápido)

```bash
# SSH al servidor
ssh root@api.guitarzone.cl

# Update código
cd /opt/guitarzone-backend
git pull origin main

# Rebuild
docker-compose -f docker-compose-prod.yml build

# Deploy (zero downtime)
docker-compose -f docker-compose-prod.yml up -d

# Migraciones si es necesario
docker-compose -f docker-compose-prod.yml exec users-service \
  python manage.py migrate

# Verificar
docker-compose -f docker-compose-prod.yml ps
curl https://api.guitarzone.cl/users-api/health/
```

---

## 📚 Flows Clave

### Registro → Verificación → Login → Compra

```
1. Usuario registra:
   POST /users-api/auth/register/
   
2. Email verificación enviado (Celery task)

3. Usuario clickea link en email:
   GET /users-api/auth/verify-email/?uidb64=...&token=...

4. Usuario loguea:
   POST /users-api/auth/login/ → get access_token

5. Usuario crea orden:
   POST /orders-api/orders/
   Authorization: access_token

6. Obtiene plan de pago:
   GET /orders-api/payment/preference/{order_id}/
   → redirige a Mercado Pago

7. Paga en MP

8. MP envía webhook:
   POST /orders-api/webhook/
   → Order status = PAID

9. Stock no se libera (pago confirmado)
```

### Orden sin Pago → Liberación de Stock

```
1. Usuario crea orden (sin pagar)
   → Order status = PENDING
   → Stock RESERVADO
   → Celery task programada (30 min)

2. Usuario abandona
   (no paga en 30 min)

3. Celery despierta:
   if Order.status == PENDING:
     → Libera stock en Products Service
     → Order status = CANCELLED
```

---

## 🌐 URLs de Acceso

| Servicio | URL |
|----------|-----|
| Users Swagger | http://localhost:7000/api/schema/swagger/ |
| Users Admin | http://localhost:7000/admin/ |
| Products Swagger | http://localhost:7100/api/schema/swagger/ |
| Products Admin | http://localhost:7100/admin/ |
| Orders Swagger | http://localhost:7200/api/schema/swagger/ |
| Orders Admin | http://localhost:7200/admin/ |
| Prod Users API | https://api.guitarzone.cl/users-api/ |
| Prod Products API | https://api.guitarzone.cl/products-api/ |
| Prod Orders API | https://api.guitarzone.cl/orders-api/ |

---

## 🔐 Variables de Entorno Críticas

```bash
# NUNCA expongas estos valores
SECRET_KEY=               # Django secret
POSTGRES_PASSWORD=        # DB password
JWT_SECRET_KEY=          # JWT signing key
INTERNAL_SERVICE_KEY=    # Inter-service auth
MERCADOPAGO_ACCESS_TOKEN= # MP API token
EMAIL_HOST_PASSWORD=     # SMTP password
RSA_PRIVATE_KEY=         # JWT private key
```

---

## 📞 Contacto y Soporte

- **GitHub**: [raul240sx/guitarzone-backend](https://github.com/raul240sx/guitarzone-backend)
- **Email**: raul.ramirezsanhueza@gmail.com
- **Issues**: Reportar en GitHub Issues
- **Docs**: Consultar README.md completo

---

**Última actualización:** Abril 2026
**Versión:** 1.0 Stable
