# GuitarZone - Guía Técnica y Arquitectura

Guía completa sobre la arquitectura de microservicios, flujos de datos y decisiones técnicas en GuitarZone.

## 📋 Tabla de Contenidos

1. [Arquitectura General](#arquitectura-general)
2. [Decisiones de Diseño](#decisiones-de-diseño)
3. [Especificaciones de Cada Servicio](#especificaciones-de-cada-servicio)
4. [Flujos de Datos Importantes](#flujos-de-datos-importantes)
5. [Base de Datos](#base-de-datos)
6. [Autenticación y Autorización](#autenticación-y-autorización)
7. [Tareas Asincrónicas](#tareas-asincrónicas)
8. [APIs RESTful](#apis-restful)
9. [Manejo de Errores](#manejo-de-errores)
10. [Optimizaciones](#optimizaciones)

---

## 🏗️ Arquitectura General

### Diagrama de Componentes

```
┌────────────────────────────────────────────────────────────────┐
│                      CLIENTE (Frontend)                        │
│                    (React, Vue, etc.)                          │
└────────────────────────┬───────────────────────────────────────┘
                         │ HTTPS
                         │
        ┌────────────────▼─────────────────────┐
        │      NGINX (Reverse Proxy)           │
        │  - Load Balancing                    │
        │  - SSL Termination                   │
        │  - Static Files                      │
        │  - Rate Limiting                     │
        └─┬──────────────┬──────────────┬──────┘
          │              │              │
    ┌─────▼───┐    ┌────▼───┐    ┌────▼────┐
    │  Users  │    │Products│    │ Orders  │
    │Service  │    │Service │    │Service  │
    │ :8000   │    │ :8000  │    │ :8000   │
    └─┬───────┘    └────┬───┘    └─┬───────┘
      │                 │          │
  ┌───▼─┐          ┌───▼───┐   ┌──▼───┐
  │Users│          │Product│   │Order │
  │ DB  │          │  DB   │   │  DB  │
  │ PG  │          │  PG   │   │  PG  │
  └─────┘          └───────┘   └──────┘

┌──────────────────────────────────────────────────────────┐
│              REDIS + CELERY (Task Queue)                 │
│  - Email Verification                                    │
│  - Stock Release                                         │
│  - Password Reset                                        │
│  - Background Jobs                                       │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│           EXTERNAL SERVICES                              │
│  - Mercado Pago (Payments)                               │
│  - SMTP Server (Email)                                   │
│  - DNS & SSL Certificates                                │
└──────────────────────────────────────────────────────────┘
```

### Características de Microservicios

| Aspecto | Detalle |
|--------|---------|
| **Aislamiento** | Cada servicio tiene su propia DB PostgreSQL |
| **Escalabilidad** | Cada servicio puede escalarse independientemente |
| **Comunicación** | HTTP REST + Header de autenticación interna |
| **Deployment** | Docker Compose orquesta todos los servicios |
| **Tareas async** | Celery para tareas en background |
| **Broker de tareas** | Redis para persistencia y sincronización |

---

## 🎯 Decisiones de Diseño

### 1. ¿Por qué 3 Bases de Datos Independientes?

**Ventajas:**
- ✅ **Escalabilidad independiente**: Crecer la DB de productos sin afectar usuarios
- ✅ **Resiliencia**: Fallo de una DB no derriba todo el sistema
- ✅ **Backup específico**: Estrategias de backup optimizadas por servicio
- ✅ **Migración facilitada**: Migrar servicio a otro servidor sin duplicar datos

**Desventajas:**
- ❌ Queries distribuidas requieren lógica en aplicación
- ❌ Transacciones distribuidas más complejas

### 2. ¿Por qué JWT con RSA?

**JWT (JSON Web Tokens)**:
- Stateless: No requiere session en DB
- Portable: Funciona entre todos los servicios
- Eficiente: Verifi­cación rápida sin DB lookup

**RSA (Rivest-Shamir-Adleman)**:
- Clave privada en Users Service (genera tokens)
- Clave pública en otros servicios (solo verifican)
- Imposible falsificar sin clave privada

```python
# Generación en Users Service (con clave privada)
token = jwt.encode(payload, private_key, algorithm='RS256')

# Verificación en Others Services (con clave pública)
jwt.decode(token, public_key, algorithms=['RS256'])
```

### 3. ¿Por qué Celery + Redis?

**Celery**:
- Procesa tareas en background sin bloquear request
- Reintentos automáticos con backoff exponencial
- Scheduled tasks para liberación de stock

**Redis**:
- Broker de mensajes robusto y rápido
- Caché distribuido
- Pub/Sub para eventos

**Casos de uso en GuitarZone**:
- Envío de emails de verificación (no bloquea registro)
- Liberación de stock tras timeout
- Recuperación de contraseña
- Notificaciones en tiempo real (futuro)

### 4. Integración Mercado Pago

**Flow:**
```
1. Cliente crea orden → Order status = PENDING
2. Backend genera preference en MP
3. Cliente redirigido a MP checkout
4. Pago procesado en MP
5. MP envía webhook a /webhook/
6. Backend verifica pago y actualiza Order status
```

**Claves de seguridad:**
- Verificación de firma en webhook
- Order verificada antes de cambiar estado
- Reintentos automáticos si tiempo está fuera

### 5. Liberación Automática de Stock

```python
# Celery Task en Orders Service
@shared_task(bind=True)
def release_stock_task(self, order_id):
    """
    Se ejecuta 30 minutos después de crear la orden.
    
    Si la orden aún está en PENDING (pago no confirmado),
    libera el stock reservado en Products Service.
    """
    order = Order.objects.get(id=order_id)
    
    if order.status == 'PENDING':
        # Llamar a Products Service
        response = requests.post(
            'http://products-service/release-stock/',
            headers={'X-Internal-Service-Key': INTERNAL_KEY},
            json={'items': order.order_items}
        )
        
        # Actualizar estado a CANCELLED
        order.status = 'CANCELLED'
        order.save()
```

---

## 🔧 Especificaciones de Cada Servicio

### Users Service (Autenticación y Perfiles)

**Modelos principales:**
```python
class User(AbstractBaseUser):
    email              # Campo único, usado para login
    first_name         # Nombre del usuario
    last_name          # Apellido del usuario
    phone              # Número de celular único
    is_verified        # Flag de verificación de email
    is_active          # Flag de cuenta activa
    is_staff           # Flag de administrador
    is_superuser       # Flag de super administrador
    deleted_at         # Timestamp del borrado lógico
    deleted_by         # Usuario que realizó el borrado
    date_joined        # Fecha de registro
    history            # Historial con django-simple-history

class Address(models.Model):
    user               # Foreign key a User
    commune            # Foreign key a Commune (ubicación)
    street             # Nombre de la calle
    number             # Número de la calle
    apartment          # Apartamento (opcional)
    is_main            # Dirección principal (único por usuario)
    is_active          # Flag de dirección activa
    deleted_at         # Timestamp del borrado lógico
    deleted_by         # Usuario que realizó el borrado
    history            # Historial

class Region(models.Model):
    name               # Nombre de región (15 en Chile)

class Commune(models.Model):
    region             # Región a la que pertenece
    name               # Nombre de comuna
```

**Endpoints principales:**

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| POST | `/auth/register/` | AllowAny | Registrar nuevo usuario |
| POST | `/auth/login/` | AllowAny | Obtener tokens JWT |
| POST | `/auth/verify-email/` | AllowAny | Verificar email |
| GET | `/users/me/` | IsAuthenticated | Datos del usuario actual |
| PATCH | `/users/me/` | IsAuthenticated | Actualizar perfil |
| POST | `/auth/change-password/` | IsAuthenticated | Cambiar contraseña |
| POST | `/auth/password-reset/` | AllowAny | Solicitar reset de password |
| POST | `/addresses/` | IsAuthenticated | Crear dirección |
| GET | `/addresses/` | IsAuthenticated | Listar direcciones del usuario |
| PATCH | `/addresses/{id}/` | IsAuthenticated | Actualizar dirección |
| DELETE | `/addresses/{id}/` | IsAuthenticated | Eliminar dirección |
| GET | `/locations/regions/` | AllowAny | Listar regiones de Chile |
| GET | `/locations/communes/` | AllowAny | Listar comunas de una región |

**Tareas Celery:**

1. **send_verification_email_task**
   - Dispara: al registrar usuario
   - Genera token de verificación
   - Envía email con link
   - Reintentos: 3 con delay de 60 segundos

2. **send_password_reset_email_task**
   - Dispara: al solicitar reset de contraseña
   - Genera token temporal
   - Envía email con link de reseteo
   - Token válido 24 horas

### Products Service (Catálogo y Stock)

**Modelos principales:**
```python
class Product(BaseModel):
    name               # Nombre del producto
    description        # Descripción detallada
    price              # Precio en CLP
    stock              # Cantidad disponible
    category           # Foreign key a Category
    measure_unit       # Foreign key a MeasureUnit
    image              # Imagen del producto (ImageField)
    created_at         # Timestamp de creación (heredado de BaseModel)
    updated_at         # Timestamp de última actualización
    state              # Flag de si está activo (borrado lógico)
    history            # Historial de cambios

class Category(BaseModel):
    name               # Nombre de categoría (ej: Guitarras, Pedales, etc)

class MeasureUnit(BaseModel):
    name               # Unidad de medida (ej: Unidad, Paquete, Set, etc)
```

**BaseModel (Herencia):**
```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)
    created_by_id = models.IntegerField(blank=True, null=True)
    updated_by_id = models.IntegerField(blank=True, null=True)
    
    class Meta:
        abstract = True
```

**Endpoints principales:**

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| GET | `/products/` | AllowAny | Listar productos (paginado, filtable) |
| GET | `/products/{id}/` | AllowAny | Obtener detalle de producto |
| POST | `/products/` | IsStaff | Crear producto |
| PATCH | `/products/{id}/` | IsStaff | Actualizar producto |
| DELETE | `/products/{id}/` | IsStaff | Eliminar producto (soft delete) |
| GET | `/categories/` | AllowAny | Listar categorías |
| POST | `/categories/` | IsStaff | Crear categoría |
| GET | `/measure-units/` | AllowAny | Listar unidades de medida |
| POST | `/measure-units/` | IsStaff | Crear unidad de medida |
| POST | `/reserve-stock/` | IsInternalService | Reservar stock (desde Orders) |
| POST | `/release-stock/` | IsInternalService | Liberar stock (desde Orders) |

**Filtros disponibles:**
```python
ProductFilter(django_filters.FilterSet):
    - category: Por categoría
    - price: Rango de precio (min_price, max_price)
    - search: Búsqueda en nombre y descripción
    - ordering: Ordenar por precio, fecha, etc.
```

**Reserva de Stock (Lógica):**
```python
# Desde Orders Service
GET /products-api/reserve-stock/
{
    "items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 3, "quantity": 1}
    ]
}

# En Products Service
for item in items:
    product = Product.objects.select_for_update().get(id=item['product_id'])
    
    if product.stock < item['quantity']:
        raise ValidationError('Stock insuficiente')
    
    product.stock -= item['quantity']
    product.save()
```

### Orders Service (Órdenes y Pagos)

**Modelos principales:**
```python
class Order(BaseModel):
    class Status(TextChoices):
        PENDING = 'PENDING'      # Esperando pago
        PAID = 'PAID'            # Pago confirmado
        CANCELLED = 'CANCELLED'  # Cancelada/Stock liberado
    
    user_id            # ID del usuario (no FK, por independencia de DBs)
    status             # Estado de la orden
    total_amount       # Total en CLP
    user_address       # ID de la dirección (desde Users Service)
    created_at         # Timestamp de creación
    updated_at         # Timestamp de actualización
    history            # Historial de cambios

class OrderDetail(models.Model):
    product_id         # ID del producto (no FK, por independencia)
    product_title      # Nombre del producto (snapshot)
    quantity           # Cantidad comprada
    unit_price         # Precio unitario en el momento (snapshot)
    image_url          # URL de la imagen (snapshot)
    order              # Foreign key a Order
    history            # Historial de cambios
```

**Endpoints principales:**

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| POST | `/orders/` | IsAuthenticated | Crear orden |
| GET | `/orders/` | IsAuthenticated | Listar órdenes del usuario |
| GET | `/orders/{id}/` | IsAuthenticated | Obtener detalle de orden |
| PATCH | `/orders/{id}/update-address/` | IsAuthenticated | Actualizar dirección de envío |
| GET | `/payment/preference/{order_id}/` | IsAuthenticated | Obtener link de pago MP |
| POST | `/webhook/` | AllowAny | Webhook de Mercado Pago |

**Flujo de Creación de Orden:**

```python
@transaction.atomic()
def create_order(user_id, order_items):
    """
    1. Valida productos en Products Service
    2. Calcula montos finales
    3. Reserva stock
    4. Crea Order y OrderDetails
    5. Programa liberación de stock en 30 min
    """
    
    # Paso 1: Consultar productos
    products_info = call_products_service(order_items)
    
    # Paso 2: Calcular total
    total_amount = sum(
        item['price'] * quantity
        for item, quantity in zip(products_info, quantities)
    )
    
    # Paso 3: Reservar stock
    reserve_stock(order_items)
    
    # Paso 4: Crear orden
    order = Order.objects.create(
        user_id=user_id,
        status=Order.Status.PENDING,
        total_amount=total_amount
    )
    
    # Crear detalles
    for item in order_items:
        OrderDetail.objects.create(
            product_id=item['product_id'],
            quantity=item['quantity'],
            unit_price=products_info[item['product_id']]['price'],
            order=order
        )
    
    # Paso 5: Agendar liberación de stock
    release_stock_task.apply_async(
        args=(order.id,),
        countdown=30*60  # 30 minutos en segundos
    )
    
    return order
```

**Integración Mercado Pago:**

```python
class MercadoPagoService:
    def create_payment_preference(self, order):
        """Genera link de pago de Mercado Pago"""
        
        items = [
            {
                'title': item.product_title,
                'quantity': item.quantity,
                'unit_price': int(item.unit_price),
                'currency_id': 'CLP'
            }
            for item in order.order_items.all()
        ]
        
        preference_data = {
            'items': items,
            'auto_return': 'approved',
            'back_urls': {
                'success': f'{FRONTEND_URL}/success/',
                'failure': f'{FRONTEND_URL}/failure/',
                'pending': f'{FRONTEND_URL}/pending/'
            },
            'external_reference': str(order.id),
            'notification_url': f'{API_URL}/orders-api/webhook/'
        }
        
        response = self.sdk.preference().create(preference_data)
        return response.get('response')
```

---

## 🔄 Flujos de Datos Importantes

### Flujo 1: Registración de Usuario

```
Frontend
   │
   ├─► [1] POST /users-api/auth/register/
   │        email, password, nombre, apellido
   │
Backend (Users Service)
   │
   ├─► [2] Valida email no exista
   ├─► [3] Hash password con PBKDF2
   ├─► [4] Crea User (is_verified=False)
   ├─► [5] Dispara Celery task: send_verification_email
   │
Celery Worker
   │
   ├─► [6] Genera token de verificación (24h)
   ├─► [7] Construye URL con token
   ├─► [8] Envía email SMTP con enlace
   │
Frontend
   │
   └─► [9] Usuario hace click en email
       [10] GET /users-api/auth/verify-email/?token=XXX
       [11] Backend verifica token y marca is_verified=True
```

### Flujo 2: Crear Orden y Pagar

```
Frontend
   │
   ├─► [1] POST /orders-api/orders/
   │        order_items: [{product_id, quantity}, ...]
   │        Authorization: Bearer JWT_TOKEN
   │
Backend (Orders Service)
   │
   ├─► [2] Autentica usuario con JWT
   │
   ├─► [3] Consulta Products Service
   │        GET /products-api/products/{id}/
   │
   ├─► [4] Extrae: nombre, precio, imagen
   │
   ├─► [5] Calcula total_amount
   │
   ├─► [6] Reserva stock en Products Service
   │        POST /products-api/reserve-stock/
   │        X-Internal-Service-Key: SECRET
   │
Backend (Products Service)
   │
   ├─► [7] Para cada item:
   │        - Obtiene producto
   │        - Decrementa stock
   │        - Valida stock >= 0
   │
   ├─► [8] Retorna 200 OK
   │
Backend (Orders Service)
   │
   ├─► [9] Dentro de @transaction.atomic():
   │        - Crea Order (status=PENDING)
   │        - Crea OrderDetails
   │
   ├─► [10] Agenda Celery task: release_stock_task
   │         (ejecutar en 30 minutos)
   │
   ├─► [11] Retorna Order creada
   │
Frontend
   │
   ├─► [12] Usuario hace click "Pagar"
   │         GET /orders-api/payment/preference/{order_id}/
   │
Backend (Orders Service)
   │
   ├─► [13] Obtiene Order de DB
   ├─► [14] Llama MercadoPagoService.create_preference()
   ├─► [15] Envía items a Mercado Pago API
   │
Mercado Pago
   │
   ├─► [16] Genera preference y devuelve init_point URL
   │
Frontend
   │
   ├─► [17] Redirige a init_point
   ├─► [18] Usuario completa pago en MP
   │
Mercado Pago
   │
   ├─► [19] Webhook → POST /orders-api/webhook/
   │         {payment_id, status, external_reference}
   │
Backend (Orders Service)
   │
   ├─► [20] Verifica firma de webhook
   ├─► [21] Consulta estado en MP API
   ├─► [22] Si status = "approved":
   │        - Order.status = PAID
   │        - Guardar payment_id
   │
   ├─► [23] Celery task se ejecuta en 30 min
   │        - Si Order.status != PENDING
   │        - No libera stock (pago fue confirmado)
```

### Flujo 3: Liberación Automática de Stock

```
[MINUTO 0] Usuario crea orden
   ├─► Order created (status=PENDING, stock reservado)
   ├─► Celery task programada (ejecutar en 30 min)
   
[MINUTO 5] Usuario abandona compra (no paga)

[MINUTO 30] Celery Worker despierta
   │
   ├─► Obtiene Order de Orders DB
   ├─► Verifica: status == PENDING ?
   │   
   │   ✓ SÍ: Stock aún reservado
   │   │   ├─► Llama Products Service
   │   │   │   POST /products-api/release-stock/
   │   │   │   X-Internal-Service-Key: SECRET
   │   │   │   {items: [{product_id, quantity}, ...]}
   │   │   │
   │   │   Backend (Products Service)
   │   │   ├─► Para cada item:
   │   │   │   - Obtiene producto
   │   │   │   - Incrementa stock
   │   │   │
   │   │   ├─► Retorna 200 OK
   │   │
   │   │   Backend (Orders Service)
   │   │   ├─► Order.status = CANCELLED
   │   │   ├─► Order.save()
   │   │
   │   ✗ NO: Pago fue confirmado
   │       ├─► Order.status = PAID
   │       └─► No hace nothing (stock permanece reservado)
```

---

## 💾 Base de Datos

### Schema - Users Service

```sql
-- users_user
CREATE TABLE users_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(9) UNIQUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    deleted_by_id INTEGER,
    date_joined TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (deleted_by_id) REFERENCES users_user(id)
);

-- locations_commune (15 regiones + 346 comunas de Chile)
CREATE TABLE locations_commune (
    id SERIAL PRIMARY KEY,
    region_id INTEGER NOT NULL,
    name VARCHAR(100),
    
    FOREIGN KEY (region_id) REFERENCES locations_region(id)
);

-- users_address
CREATE TABLE users_address (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    commune_id INTEGER NOT NULL,
    street VARCHAR(100),
    number VARCHAR(10),
    apartment VARCHAR(10) NULL,
    is_main BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    deleted_at TIMESTAMP NULL,
    deleted_by_id INTEGER,
    
    FOREIGN KEY (user_id) REFERENCES users_user(id),
    FOREIGN KEY (commune_id) REFERENCES locations_commune(id),
    FOREIGN KEY (deleted_by_id) REFERENCES users_user(id),
    
    UNIQUE (user_id) WHERE is_main=TRUE AND is_active=TRUE
);
```

### Schema - Products Service

```sql
-- products_category
CREATE TABLE products_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    state BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER,
    updated_by_id INTEGER
);

-- products_measureunit
CREATE TABLE products_measureunit (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    state BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER,
    updated_by_id INTEGER
);

-- products_product
CREATE TABLE products_product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description TEXT,
    price DECIMAL(10, 2),
    stock BIGINT DEFAULT 0,
    category_id INTEGER,
    measure_unit_id INTEGER,
    image VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    state BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER,
    updated_by_id INTEGER,
    
    FOREIGN KEY (category_id) REFERENCES products_category(id),
    FOREIGN KEY (measure_unit_id) REFERENCES products_measureunit(id)
);

-- Índices para performance
CREATE INDEX idx_product_category ON products_product(category_id);
CREATE INDEX idx_product_state ON products_product(state);
```

### Schema - Orders Service

```sql
-- orders_order
CREATE TABLE orders_order (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    total_amount DECIMAL(8, 0),
    user_address INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    state BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER,
    updated_by_id INTEGER,
    
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);

-- orders_orderdetail
CREATE TABLE orders_orderdetail (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    product_title VARCHAR(50),
    quantity INTEGER,
    unit_price DECIMAL(8, 0),
    image_url TEXT,
    order_id INTEGER NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders_order(id) ON DELETE CASCADE
);
```

### Índices de Performance

```sql
-- Users Service
CREATE INDEX idx_user_email ON users_user(email);
CREATE INDEX idx_user_is_verified ON users_user(is_verified);
CREATE INDEX idx_address_user ON users_address(user_id);

-- Products Service
CREATE INDEX idx_product_stock ON products_product(stock);
CREATE INDEX idx_product_price ON products_product(price);

-- Orders Service
CREATE INDEX idx_order_user_id ON orders_order(user_id);
CREATE INDEX idx_order_status ON orders_order(status);
CREATE INDEX idx_orderdetail_order ON orders_orderdetail(order_id);
```

---

## 🔐 Autenticación y Autorización

### JWT con RSA Asimétrico

**Generación de tokens (Users Service):**

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        
        # Agregar claims personalizados
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        
        return token

# En settings.py:
SIMPLE_JWT = {
    'ALGORITHM': 'RS256',
    'SIGNING_KEY': RSA_PRIVATE_KEY,
    'VERIFYING_KEY': RSA_PUBLIC_KEY,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

**Verificación de tokens (Products y Orders Services):**

```python
class RSAAuthentication(authentication.TokenAuthentication):
    """Autentica tokens JWT con clave pública RSA"""
    
    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(
                key,
                settings.RSA_PUBLIC_KEY,
                algorithms=['RS256']
            )
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('Firma inválida')
        except (jwt.DecodeError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed('Token inválido')
        
        return (user, key)
```

### Permisos Personalizados

**IsStaffPermission (Products Service):**
```python
class IsStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Solo staff puede crear/editar/eliminar
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_staff
        
        # GET es público
        return True
```

**IsInternalService (Ambos):**
```python
class IsInternalService(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verifica header X-Internal-Service-Key
        header = request.META.get('HTTP_X_INTERNAL_SERVICE_KEY')
        return header == settings.INTERNAL_SERVICE_KEY
```

---

## 🔄 Tareas Asincrónicas

### Configuración Celery

**users_project/celery.py:**
```python
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_project.settings.production')

app = Celery('users_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configuración
CELERY_BROKER_URL = 'redis://redis-service:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis-service:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

### Tareas Definidas

**Users Service:**

```python
@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
    name='send_verification_email_task'
)
def send_verification_email_task(self, user_id):
    """Envía email de verificación a nuevo usuario"""
    try:
        user = User.objects.get(id=user_id)
        
        if user.is_verified:
            return "User already verified"
        
        token = EmailVerificationTokenGenerator().make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        
        verify_link = f'{settings.SITE_URL}/verify-email?uidb64={uidb64}&token={token}'
        
        send_transactional_email(
            subject='Verifica tu cuenta en GuitarZone',
            email_to=user.email,
            template_name='emails/verification_email.html',
            context={'verify_link': verify_link, 'username': user.email}
        )
        
        return f"Verification email sent to {user.email}"
    
    except Exception as e:
        # Reintenta con backoff exponencial
        raise self.retry(exc=e, countdown=60)
```

**Orders Service:**

```python
@shared_task(
    bind=True,
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    max_retries=3,
    default_retry_delay=30
)
def release_stock_task(self, order_id):
    """
    Libera stock 30 minutos después de crear la orden.
    Se ejecuta si la orden aún está en estado PENDING.
    """
    try:
        order = Order.objects.get(id=order_id, state=True)
        
        if order.status != Order.Status.PENDING:
            return f"Order {order_id} already has status {order.status}"
        
        # Prepara items para liberar
        items = [
            {'product_id': item.product_id, 'quantity': item.quantity}
            for item in order.order_items.all()
        ]
        
        # Llamada a Products Service
        response = requests.post(
            settings.PRODUCTS_RELEASE_STOCK,
            json={'items': items},
            headers={
                'X-Internal-Service-Key': settings.INTERNAL_SERVICE_KEY,
                'Content-Type': 'application/json'
            },
            timeout=5
        )
        
        if response.status_code == 200:
            order.status = Order.Status.CANCELLED
            order.save()
            return f"Stock released for order {order_id}"
        else:
            raise requests.RequestException(
                f"Products service error: {response.status_code}"
            )
    
    except Order.DoesNotExist:
        return f"Order {order_id} not found"
    except Exception as e:
        raise self.retry(exc=e)
```

---

## 🚀 APIs RESTful

### Standard Response Format

**Respuesta exitosa (GET /products/{id}/):**
```json
{
    "id": 1,
    "name": "Guitarra Acústica Premium",
    "description": "Guitarra acústica de madera maciza",
    "price": 199999.99,
    "stock": 5,
    "category": {
        "id": 1,
        "name": "Guitarras Acústicas"
    },
    "measure_unit": {
        "id": 1,
        "name": "Unidad"
    },
    "image": "/media/products/guitar_acoustic.jpg",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-16T14:20:00Z",
    "state": true
}
```

**Respuesta con error:**
```json
{
    "detail": "Not Found",
    "status_code": 404
}
```

### Paginación

**Query params:**
```
GET /products-api/products/?page=2&page_size=20

Response:
{
    "count": 245,
    "next": "https://api.guitarzone.cl/products-api/products/?page=3&page_size=20",
    "previous": "https://api.guitarzone.cl/products-api/products/?page=1&page_size=20",
    "results": [...]
}
```

### Filtrado y Búsqueda

```
GET /products-api/products/?category=1&min_price=50000&max_price=300000&search=guitarra&ordering=-price

Filtros disponibles:
- category: ID de categoría
- min_price / max_price: Rango de precio
- search: Búsqueda por nombre o descripción
- ordering: Ordenamiento (-price, created_at, etc.)
```

---

## ❌ Manejo de Errores

### Excepciones Personalizadas

```python
# apps/base/exceptions.py

class PaymentError(Exception):
    """Error durante procesamiento de pago"""
    pass

class StockError(Exception):
    """Error relacionado con inventario"""
    pass

class AuthenticationError(Exception):
    """Error de autenticación entre servicios"""
    pass
```

### Middleware de Errores

```python
class CustomExceptionMiddleware:
    """Middleware que captura y formatea errores comunes"""
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
        except ValidationError as e:
            return JsonResponse({
                'error': 'Validation Error',
                'detail': str(e),
                'status': 400
            }, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({
                'error': 'Not Found',
                'detail': str(e),
                'status': 404
            }, status=404)
        
        return response
```

---

## ⚡ Optimizaciones

### Select Related & Prefetch Related

```python
# Products Service
def get_queryset(self):
    return Product.objects.filter(state=True)\
        .select_related('category', 'measure_unit')\
        .prefetch_related('history')
```

### Caching

```python
# Redis cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutos
def get_categories(request):
    categories = Category.objects.filter(state=True)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
```

### Transaciones Atómicas

```python
# Orders Service - Crear orden
@transaction.atomic()
def create_order_and_detail(user_id, total_amount, order_items_info):
    """
    Asegura que si algo falla, todo rollback
    """
    order = Order.objects.create(
        user_id=user_id,
        total_amount=total_amount,
        status=Order.Status.PENDING
    )
    
    details = [
        OrderDetail(...) for item in order_items_info.values()
    ]
    
    OrderDetail.objects.bulk_create(details)
    
    return order
```

### Select for Update

```python
# Products Service - Reservar stock
product = Product.objects.select_for_update().get(id=product_id)

if product.stock < quantity:
    raise ValidationError('Insufficient stock')

product.stock -= quantity
product.save()
```

---

## 📚 Referencias

- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django Simple History](https://django-simple-history.readthedocs.io/)
- [Celery](https://docs.celeryproject.org/)
- [Mercado Pago SDK](https://github.com/mercadopago/sdk-python)
- [JWT & RS256](https://tools.ietf.org/html/rfc7519)

---

**Última actualización:** Abril 2026
