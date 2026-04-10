# GuitarZone - E-Commerce API

Plataforma de e-commerce especializada en la venta de productos y accesorios musicales exclusivos para guitarristas. Sistema backend escalable basado en microservicios que permite la gestión integral de usuarios, catálogo de productos y procesamiento de órdenes de compra con integración de pasarela de pago.

## 🚀 Características principales

### 🔐 Gestión de Usuarios (Users Service)
- **Registro y autenticación segura**: Sistema de autenticación basado en tokens JWT con cifrado RSA de 2048 bits
- **Verificación de email**: Todos los usuarios deben verificar su correo mediante enlace de verificación antes de realizar compras
- **Gestión de perfiles**: Actualización de datos personales (nombre, apellido, teléfono)
- **Administración de direcciones**: Sistema completo de direcciones con soporte para direcciones principales
- **Base de datos de ubicaciones**: Base integrada de todas las Regiones y Comunas de Chile para facilitar la creación de direcciones
- **Recuperación de contraseña**: Sistema de reset de contraseña mediante email
- **Borrado lógico de usuarios**: Preservación de datos históricos mediante eliminación suave
- **Generación automática de username**: Sistema que genera automáticamente un nombre de usuario que puede ser personalizado posteriormente

### 📦 Gestión de Productos (Products Service)
- **CRUD completo de productos**: Crear, leer, actualizar y eliminar productos
- **Gestión de inventario**: Control preciso del stock disponible
- **Categorización de productos**: Organización mediante categorizas personalizables
- **Unidades de medida**: Sistema flexible de unidades (Unidades, Paquetes, Sets, etc.)
- **Gestión de imágenes**: Carga y almacenamiento de imágenes de productos
- **Filtrado y búsqueda avanzada**: Búsqueda por nombre, descripción y filtrado por categoría y precio
- **Reserva de stock**: API dedicada para reservar productos antes de procesar pagos
- **Liberación de stock**: Liberación automática de stock tras timeout o cancelación de órdenes
- **Vistas públicas**: Catálogo disponible para usuarios no autenticados

### 🛒 Gestión de Órdenes (Orders Service)
- **Creación de órdenes**: Sistema transaccional para crear órdenes con múltiples productos
- **Reserva automática de stock**: Al crear una orden, se reserva automáticamente el stock del servicio de productos
- **Cálculo de montos**: Cálculo automático del total de la orden basado en precios y cantidades
- **Estados de órdenes**: Estados completos (Pendiente, Pagado, Cancelado)
- **Integración con Mercado Pago**: Procesamiento de pagos mediante API de Mercado Pago
- **Webhook de pagos**: Notificaciones automáticas de estado de pagos desde Mercado Pago
- **Gestión de direcciones de envío**: Vinculación de direcciones del usuario a las órdenes
- **Liberación automática de stock**: Tarea programada con Celery que libera stock después del timeout
- **Trazabilidad completa**: Historial de cambios en todas las órdenes y detalles

### ⚙️ Infraestructura de Tareas
- **Tareas asincrónicas**: Procesamiento de tareas en background con Celery y Redis
- **Notificaciones por email**: Envío de correos transaccionales (verificación, recuperación de contraseña)
- **Reintentos automáticos**: Sistema de reintentos con backoff exponencial
- **Programación de trabajos**: Liberación automática de stock tras timeout

## 🛠️ Tecnologías utilizadas

### Backend
- **Framework**: Django 4.2+ con Django Rest Framework (DRF)
- **Base de datos**: PostgreSQL 15 (3 instancias independientes)
- **API REST**: Django Rest Framework con documentación automática (Swagger)
- **Autenticación**: JWT (JSON Web Tokens) con cryptography y PyJWT
- **Tareas asincrónicas**: Celery con Redis como broker
- **Notificaciones**: Integración de email transaccional
- **Pasarela de pago**: SDK oficial de Mercado Pago
- **Validación**: Django filters, Serializers validados
- **Versionado de datos**: django-simple-history para auditoría
- **CORS**: django-cors-headers para comunicación entre servicios

### DevOps & Deployment
- **Contenedores**: Docker y Docker Compose
- **Servidor web**: Gunicorn (WSGI)
- **Proxy inverso**: Nginx como reverse proxy
- **Cache**: Redis (Broker de Celery)
- **Control de versiones**: Git & GitHub
- **Ambiente**: Archivo .env para configuración por entorno (desarrollo/producción)

### Herramientas de documentación
- **API Documentation**: drf-spectacular (Swagger/OpenAPI 3.0)
- **Control de acceso**: Permissions personalizados basados en roles
- **Middlewares**: Autenticación personalizada entre servicios

## 📂 Estructura del proyecto

```
ecommerce_backend_production/
├── backend/
│   │
│   ├── users/                          # Users Service
│   │   ├── dockerfile                  # Imagen Docker del servicio
│   │   ├── entrypoint.sh               # Punto de entrada del contenedor
│   │   ├── manage.py                   # CLI de Django
│   │   ├── requirements.txt            # Dependencias Python
│   │   ├── .env                        # Variables de entorno (local)
│   │   ├── apps/
│   │   │   ├── users/                  # App de gestión de usuarios
│   │   │   │   ├── models/
│   │   │   │   │   ├── user.py         # Modelo User (AbstractBaseUser)
│   │   │   │   │   └── address.py      # Modelo Address
│   │   │   │   ├── views/              # Vistas y ViewSets
│   │   │   │   ├── serializers/        # Serializadores (User, Address, Tokens)
│   │   │   │   ├── permissions/        # Permisos personalizados
│   │   │   │   ├── tokens/             # Generadores de tokens JWT
│   │   │   │   ├── tasks/              # Tareas Celery
│   │   │   │   │   ├── email_verification.py      # Envío de emails de verificación
│   │   │   │   │   └── password_reset.py          # Recuperación de contraseña
│   │   │   │   ├── services/           # Lógica de negocio
│   │   │   │   ├── urls.py             # Rutas de la app
│   │   │   │   ├── admin.py            # Panel de administración
│   │   │   │   └── migrations/
│   │   │   │
│   │   │   ├── locations/              # App de ubicaciones
│   │   │   │   ├── models.py           # Modelos Region y Commune
│   │   │   │   ├── views/              # ViewSets para regiones y comunas
│   │   │   │   ├── serializers/        # Serializadores
│   │   │   │   ├── urls.py
│   │   │   │   └── migrations/
│   │   │   │
│   │   │   └── base/                   # App base compartida
│   │   │       ├── models.py           # Modelo base para auditoría
│   │   │       ├── middleware.py       # Middlewares personalizados
│   │   │       ├── custom_authentication.py  # Autenticación personalizada
│   │   │       └── permissions/        # Permisos base
│   │   │
│   │   └── users_project/              # Configuración principal de Django
│   │       ├── settings/
│   │       │   ├── base.py             # Configuración base
│   │       │   ├── local.py            # Configuración desarrollo
│   │       │   └── production.py       # Configuración producción
│   │       ├── urls.py                 # Rutas principales
│   │       ├── celery.py               # Configuración Celery
│   │       ├── asgi.py                 # ASGI para async
│   │       └── wsgi.py                 # WSGI para Gunicorn
│   │
│   ├── products/                       # Products Service
│   │   ├── dockerfile
│   │   ├── entrypoint.sh
│   │   ├── manage.py
│   │   ├── requirements.txt
│   │   ├── .env
│   │   ├── apps/
│   │   │   ├── products/               # App de gestión de productos
│   │   │   │   ├── models/
│   │   │   │   │   ├── product.py      # Modelo Product
│   │   │   │   │   ├── category.py     # Modelo Category
│   │   │   │   │   └── measure_unit.py # Modelo MeasureUnit
│   │   │   │   ├── views/
│   │   │   │   │   ├── product_viewset.py        # CRUD de productos
│   │   │   │   │   ├── reserve_stock_view.py     # Reserva de stock
│   │   │   │   │   ├── release_stock_view.py     # Liberación de stock
│   │   │   │   │   ├── category_viewset.py       # CRUD de categorías
│   │   │   │   │   └── measure_unit_viewset.py   # CRUD de unidades de medida
│   │   │   │   ├── serializers/        # Serializadores
│   │   │   │   ├── filters.py          # Filtros avanzados
│   │   │   │   ├── permissions/        # Permisos (IsStaff, IsInternalService)
│   │   │   │   ├── urls.py
│   │   │   │   ├── admin.py
│   │   │   │   └── migrations/
│   │   │   │
│   │   │   └── base/                   # App base compartida
│   │   │       ├── models.py           # Modelo base
│   │   │       ├── middleware.py
│   │   │       └── custom_authentication.py
│   │   │
│   │   └── products_project/           # Configuración principal Django
│   │       ├── settings/
│   │       │   ├── base.py
│   │       │   ├── local.py
│   │       │   └── production.py
│   │       ├── urls.py
│   │       ├── asgi.py
│   │       └── wsgi.py
│   │
│   └── orders/                         # Orders Service
│       ├── dockerfile
│       ├── entrypoint.sh
│       ├── manage.py
│       ├── requirements.txt
│       ├── .env
│       ├── apps/
│       │   ├── orders/                 # App de gestión de órdenes
│       │   │   ├── models/
│       │   │   │   ├── order.py        # Modelo Order (estados, montos)
│       │   │   │   └── order_detail.py # Modelo OrderDetail (items de la orden)
│       │   │   ├── views/
│       │   │   │   ├── order_create_view.py           # Crear órdenes
│       │   │   │   ├── order_list_view.py             # Listar órdenes del usuario
│       │   │   │   ├── order_view.py                  # Detalles de orden
│       │   │   │   ├── order_update_address_view.py   # Actualizar dirección de envío
│       │   │   │   ├── mp_payment_view.py             # Iniciar pago Mercado Pago
│       │   │   │   └── mp_webhook_view.py             # Webhook de Mercado Pago
│       │   │   ├── serializers/        # Serializadores
│       │   │   ├── services/
│       │   │   │   ├── consult_produts_service.py     # Consulta de productos
│       │   │   │   └── mercadopago_service.py         # Integración MP
│       │   │   ├── tasks/
│       │   │   │   └── release_stock_task.py          # Liberación automática de stock
│       │   │   ├── urls.py
│       │   │   ├── admin.py
│       │   │   └── migrations/
│       │   │
│       │   └── base/                   # App base compartida
│       │       ├── models.py           # Modelo base
│       │       ├── middleware.py
│       │       ├── exceptions.py        # Excepciones personalizadas
│       │       └── custom_authentication.py
│       │
│       └── orders_project/             # Configuración principal Django
│           ├── settings/
│           │   ├── base.py
│           │   ├── local.py
│           │   └── production.py
│           ├── urls.py
│           ├── celery.py               # Configuración Celery
│           ├── asgi.py
│           └── wsgi.py
│
├── media/                              # Archivos media por servicio
│   ├── orders/
│   ├── products/
│   └── users/
│
├── secrets/                            # Claves y secretos (no versionado)
│   ├── orders/
│   ├── products/
│   └── users/
│
├── nginx/
│   └── default.conf                    # Configuración Nginx como reverse proxy
│
├── docker-compose.yml                  # Orquestación desarrollo
├── docker-compose-prod.yml             # Orquestación producción
├── README.md                           # Introducción al proyecto
└── .gitignore                          # Archivos a ignorar en git
```

## ⚙️ Instalación y configuración

La forma recomendada de correr este proyecto es mediante Docker Compose. No es necesario crear entornos virtuales manualmente.

### 1. Clonar repositorio

```bash
git clone https://github.com/raul240sx/guitarzone-backend.git
cd guitarzone-backend
```

### 2. Configurar archivos .env

Debes crear archivos `.env` en cada servicio:

📌 **En la raíz del proyecto (.env para docker-compose.yml)**:

```env
# Base de datos
POSTGRES_USER=guitarzone_user
POSTGRES_PASSWORD=tu_contraseña_segura_aqui
```

📌 **En backend/users/.env**:

```env
# Django
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,api.guitarzone.cl

# Database
DATABASE_URL=postgresql://guitarzone_user:tu_contraseña@users-db:5432/users_db

# JWT & RSA Keys
JWT_SECRET_KEY=tu_jwt_secret_key_aqui
RSA_PUBLIC_KEY_PATH=/run/secrets/rsa_public_key.pem
RSA_PRIVATE_KEY_PATH=/run/secrets/rsa_private_key.pem

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_aqui
SITE_NAME=GuitarZone
SITE_URL=https://guitarzone.cl
VERIFY_URL_PATH=verify-email

# Redis
REDIS_URL=redis://redis-service:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://guitarzone.cl

# Internal Service Communication
PRODUCTS_SERVICE_URL=http://products-service:8000
ORDERS_SERVICE_URL=http://orders-service:8000
INTERNAL_SERVICE_KEY=tu_clave_interna_segura_aqui
```

📌 **En backend/products/.env**:

```env
# Django
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,api.guitarzone.cl

# Database
DATABASE_URL=postgresql://guitarzone_user:tu_contraseña@products-db:5432/products_db

# JWT & RSA Keys
JWT_SECRET_KEY=tu_jwt_secret_key_aqui
RSA_PUBLIC_KEY_PATH=/run/secrets/rsa_public_key.pem

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://guitarzone.cl

# Internal Service Communication
INTERNAL_SERVICE_KEY=tu_clave_interna_segura_aqui
```

📌 **En backend/orders/.env**:

```env
# Django
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,api.guitarzone.cl

# Database
DATABASE_URL=postgresql://guitarzone_user:tu_contraseña@orders-db:5432/orders_db

# JWT & RSA Keys
JWT_SECRET_KEY=tu_jwt_secret_key_aqui
RSA_PUBLIC_KEY_PATH=/run/secrets/rsa_public_key.pem

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=tu_access_token_mp_aqui
FRONTEND_URL=https://guitarzone.cl

# Redis
REDIS_URL=redis://redis-service:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://guitarzone.cl

# Internal Service Communication
PRODUCTS_SERVICE_URL=http://products-service:8000
PRODUCTS_RESERVE_STOCK=http://products-service:8000/products-api/reserve-stock/
PRODUCTS_RELEASE_STOCK=http://products-service:8000/products-api/release-stock/
INTERNAL_SERVICE_KEY=tu_clave_interna_segura_aqui
```

⚠️ **Importante**: 
- Reemplaza todos los valores entre `tu_*_aqui` con valores reales
- La `SECRET_KEY` debe ser única y secreta (genera una en [djecrety.ir](https://djecrety.ir/))
- Usa contraseñas fuertes para la base de datos
- Nunca commits los archivos `.env` a git

### 3. Generar claves RSA para JWT (solo primera vez)

```bash
# Generar clave privada
openssl genrsa -out rsa_private_key.pem 2048

# Generar clave pública desde la privada
openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem

# Copiar las claves a los directorios de secrets
cp rsa_private_key.pem secrets/users/
cp rsa_public_key.pem secrets/users/
cp rsa_public_key.pem secrets/products/
cp rsa_public_key.pem secrets/orders/
```

### 4. Levantar contenedores (Desarrollo)

```bash
# Desarrollo
docker-compose up --build

# Producción
docker-compose -f docker-compose-prod.yml up --build -d
```

El proyecto quedará disponible en:
- **API**: `http://localhost:7000` (users), `http://localhost:7100` (products), `http://localhost:7200` (orders)
- **Swagger**: `http://localhost:7000/api/schema/swagger/`
- **Nginx (Prod)**: `https://api.guitarzone.cl`

### 5. Ejecutar migraciones

```bash
# Users service
docker-compose exec users-service python manage.py migrate

# Products service
docker-compose exec products-service python manage.py migrate

# Orders service
docker-compose exec orders-service python manage.py migrate
```

### 6. Crear superusuario

```bash
docker-compose exec users-service python manage.py createsuperuser
```

### 7. Cargar datos iniciales (opcional)

```bash
# Regiones y comunas de Chile
docker-compose exec users-service python manage.py loaddata regions_communes

# Categorías de productos
docker-compose exec products-service python manage.py loaddata product_categories
```

## 📖 Uso de la aplicación

### Users Service (`/users-api/`)

#### Autenticación
```bash
# Registrar nuevo usuario
POST /users-api/auth/register/
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña_segura",
  "first_name": "Juan",
  "last_name": "Pérez"
}

# Login
POST /users-api/auth/login/
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña_segura"
}
# Respuesta: { "access": "token_jwt", "refresh": "token_refresh" }

# Verificar email
POST /users-api/auth/verify-email/
{
  "uidb64": "...",
  "token": "..."
}
```

#### Perfil de Usuario
```bash
# Obtener datos del usuario
GET /users-api/users/me/
Authorization: Bearer <access_token>

# Actualizar perfil
PATCH /users-api/users/me/
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "phone": "912345678"
}

# Cambiar contraseña
POST /users-api/auth/change-password/
{
  "old_password": "contraseña_vieja",
  "new_password": "contraseña_nueva"
}

# Recuperar contraseña
POST /users-api/auth/password-reset/
{
  "email": "usuario@ejemplo.com"
}
```

#### Gestión de Direcciones
```bash
# Crear dirección
POST /users-api/addresses/
{
  "commune_id": 1,
  "street": "Calle Principal",
  "number": "123",
  "apartment": "A",
  "is_main": true
}

# Obtener direcciones del usuario
GET /users-api/addresses/
Authorization: Bearer <access_token>

# Actualizar dirección
PATCH /users-api/addresses/{id}/

# Eliminar dirección
DELETE /users-api/addresses/{id}/
```

#### Ubicaciones
```bash
# Obtener regiones de Chile
GET /users-api/locations/regions/

# Obtener comunas de una región
GET /users-api/locations/communes/?region_id=1
```

### Products Service (`/products-api/`)

#### Productos
```bash
# Listar productos (público)
GET /products-api/products/
?category=1&min_price=10000&max_price=100000&ordering=-price&search=guitarra

# Obtener detalle de producto
GET /products-api/products/{id}/

# Crear producto (solo staff)
POST /products-api/products/
Authorization: Bearer <access_token>
{
  "name": "Guitarra Acústica",
  "description": "Guitarra acústica de calidad profesional",
  "price": 150000.00,
  "stock": 10,
  "category_id": 1,
  "measure_unit_id": 1,
  "image": <archivo>
}

# Actualizar producto (solo staff)
PATCH /products-api/products/{id}/

# Eliminar producto (soft delete, solo staff)
DELETE /products-api/products/{id}/
```

#### Gestión de Stock (Interno)
```bash
# Reservar stock (llamada interna desde orders-service)
POST /products-api/reserve-stock/
X-Internal-Service-Key: <internal_key>
{
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 3, "quantity": 1}
  ]
}

# Liberar stock (llamada interna desde orders-service)
POST /products-api/release-stock/
X-Internal-Service-Key: <internal_key>
{
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 3, "quantity": 1}
  ]
}
```

### Orders Service (`/orders-api/`)

#### Órdenes
```bash
# Crear orden
POST /orders-api/orders/
Authorization: Bearer <access_token>
{
  "order_items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 3, "quantity": 1}
  ]
}

# Listar órdenes del usuario
GET /orders-api/orders/
Authorization: Bearer <access_token>

# Obtener detalle de orden
GET /orders-api/orders/{id}/
Authorization: Bearer <access_token>

# Actualizar dirección de envío
PATCH /orders-api/orders/{id}/update-address/
{
  "user_address": 2
}
```

#### Pagos (Mercado Pago)
```bash
# Obtener preferencia de pago
GET /orders-api/payment/preference/{order_id}/
Authorization: Bearer <access_token>
# Respuesta: { "init_point": "https://www.mercadopago.com/..." }

# Webhook de notificación de pago
POST /orders-api/webhook/
X-Signature: <firma>
```

## 🔄 Flujo de Compra Completo

1. **Usuario registrado y verificado** → Crea una cuenta y verifica su email
2. **Explora catálogo** → Consulta productos disponibles (sin autenticación)
3. **Selecciona productos** → Realiza reserva interna de stock
4. **Crea orden** → POST a `/orders-api/orders/` con items seleccionados
   - Sistema consulta precios actuales a products-service
   - Reserva stock en products-service
   - Crea orden y detalles en orders-service
5. **Inicia pago** → GET a `/orders-api/payment/preference/{order_id}/`
   - Servidor genera preferencia en Mercado Pago
   - Usuario es redirigido a checkout de MP
6. **Paga en Mercado Pago** → Usuario completa el pago
7. **Webhook de confirmación** → MP notifica a orders-service
   - Order pasa a estado `PAID`
8. **Liberación automática de stock** → Si la orden no es pagada en 30 minutos:
   - Celery ejecuta `release_stock_task`
   - Stock es devuelto a products-service
   - Order pasa a estado `CANCELLED`


**Autenticación entre servicios**: Mediante header `X-Internal-Service-Key` (clave compartida)

## 🔒 Seguridad

- **JWT con RSA**: Tokens firmados con criptografía RSA 2048 bits
- **HTTPS en producción**: Protección SSL/TLS con Nginx
- **CORS configurado**: Solo orígenes permitidos
- **Claves compartidas**: Comunicación interna autenticada
- **Borrado lógico**: Preservación de datos históricos
- **Validación de entrada**: Serializers con validaciones estrictas
- **Permisos granulares**: Basados en roles (staff, usuario normal)
- **Rate limiting**: Control de solicitudes (configurable)

## 🔮 Mejoras futuras

- **Dashboard administrativo**: Panel para dueño de tienda con métricas de ventas, ingresos, productos más vendidos
- **Campos adicionales en dirección**: Referencia de ubicación, instrucciones de entrega, horario de recepción
- **Generación de boletas**: Emisión automática de boletas tributarias en formato PDF
- **Envío de emails con detalles**: Notificación de orden, respuesta de confirmación de pago, envío de link de seguimiento
- **Seguimiento de envíos**: Integración con sistema de courier (DHL, Starken, etc.)
- **Análisis y reportes**: Dashboard con KPIs, gráficos de ventas, comportamiento de clientes
- **Sistema de reseñas**: Calificaciones y comentarios de productos por usuarios
- **Carrito persistente**: Almacenamiento de carrito en la plataforma
- **Wishlist**: Productos favoritos para usuarios autenticados
- **Descuentos y cupones**: Sistema de códigos de descuento
- **Notificaciones en tiempo real**: WebSockets para actualizaciones de estado de orden
- **Integración de múltiples pasarelas**: PayPal, Stripe, Webpay
- **Gestión de devoluciones**: Sistema de RMA (Return Merchandise Authorization)
- **Historial de compras**: Reporte detallado de todas las transacciones del usuario

## 📝 Notas de Deployment

### Producción con Docker Compose

```bash
# Construir imágenes
docker-compose -f docker-compose-prod.yml build

# Levantar servicios en background
docker-compose -f docker-compose-prod.yml up -d

# Ver logs
docker-compose -f docker-compose-prod.yml logs -f

# Detener servicios
docker-compose -f docker-compose-prod.yml down
```

### Monitoreo

```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs de servicio específico
docker-compose logs users-service

# Ver logs de Celery
docker-compose logs users-celery
```

### Backups

```bash
# Backup de base de datos Users
docker-compose exec users-db pg_dump -U guitarzone_user users_db > backup_users.sql

# Restaurar backup
docker-compose exec -T users-db psql -U guitarzone_user users_db < backup_users.sql
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para colaborar:

1. Haz un fork del proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Estándares de código

- Usar PEP 8 para Python
- Documentar funciones y clases
- Agregar tests para nuevas funcionalidades
- Mantener historiales limpios de commits

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente, siempre mencionando al autor original.

## 👨‍💻 Autor

**Raúl Ignacio Ramírez Sanhueza**

- GitHub: [@raul240sx](https://github.com/raul240sx)
- Email: raul.ramirezsanhueza@gmail.com
- Sitio web: [guitarzone.cl](https://guitarzone.cl)

---

**Última actualización**: Abril 2026

Para más información sobre características específicas o problemas de configuración, consulta la documentación API en `/api/schema/swagger/` cuando el proyecto esté funcionando.
