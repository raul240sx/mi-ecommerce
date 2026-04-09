# GuitarZone - Modelos y Serializers (Referencia)

Referencia completa de los modelos de datos y sus serializadores.

---

## 📋 Tabla de Contenidos

1. [Users Service Data Models](#users-service-data-models)
2. [Products Service Data Models](#products-service-data-models)
3. [Orders Service Data Models](#orders-service-data-models)
4. [Serializers](#serializers)
5. [Relaciones entre Modelos](#relaciones-entre-modelos)
6. [Valores por Defecto y Validaciones](#valores-por-defecto-y-validaciones)

---

## 👤 Users Service Data Models

### Model: User

**Descripción**: Modelo personalizado de usuario basado en AbstractBaseUser.

**Campos:**

| Campo | Tipo | Nulo | Único | Default | Descripción |
|-------|------|------|-------|---------|-------------|
| `id` | AutoField | No | Sí | Auto | Identificador único |
| `password` | CharField | No | No | - | Contraseña hasheada (PBKDF2) |
| `last_login` | DateTimeField | Sí | No | NULL | Último acceso a la plataforma |
| `email` | EmailField | No | Sí | - | Correo electrónico del usuario |
| `first_name` | CharField | Sí | No | '' | Nombre del usuario |
| `last_name` | CharField | Sí | No | '' | Apellido del usuario |
| `phone` | CharField | Sí | Sí | NULL | Teléfono celular (9 dígitos) |
| `is_verified` | BooleanField | No | No | False | Flag de verificación de email |
| `is_active` | BooleanField | No | No | True | Flag de cuenta activa |
| `is_staff` | BooleanField | No | No | False | Flag de administrador |
| `is_superuser` | BooleanField | No | No | False | Flag de super administrador |
| `deleted_at` | DateTimeField | Sí | No | NULL | Timestamp de borrado lógico |
| `deleted_by_id` | ForeignKey | Sí | No | NULL | Referencia al usuario que borró |
| `date_joined` | DateTimeField | No | No | NOW() | Fecha de registro |
| `history` | HistoricalRecords | - | - | - | Auditoría de cambios |

**Métodos:**

```python
@property
def is_profile_complete():
    """Verifica si perfil tiene nombre, apellido, teléfono y al menos una dirección"""
    
class UserManager:
    def create_user(email, password, **extra_fields)
    def create_superuser(email, password, **extra_fields)

def soft_delete(actor=None)
    """Realiza borrado lógico (is_active=False, deleted_at=NOW())"""

def delete(using=None, keep_parents=False, actor=None)
    """Override de delete() para usar soft_delete"""
```

**Índices:**
```sql
CREATE UNIQUE INDEX idx_user_email ON users_user(email);
CREATE INDEX idx_user_is_verified ON users_user(is_verified);
```

---

### Model: Address

**Descripción**: Dirección de envío del usuario.

**Campos:**

| Campo | Tipo | Nulo | Unique | Default | Descripción |
|-------|------|------|--------|---------|-------------|
| `id` | AutoField | No | Sí | Auto | Identificador único |
| `user_id` | ForeignKey | No | No | - | Referencia al Usuario |
| `commune_id` | ForeignKey | No | No | - | Referencia a Commune (ubicación) |
| `street` | CharField | No | No | - | Nombre de la calle |
| `number` | CharField | No | No | - | Número del domicilio |
| `apartment` | CharField | Sí | No | NULL | Número de apartamento (opcional) |
| `is_main` | BooleanField | No | No | False | Dirección principal del usuario |
| `is_active` | BooleanField | No | No | True | Flag de dirección activa |
| `deleted_at` | DateTimeField | Sí | No | NULL | Timestamp de borrado |
| `deleted_by_id` | ForeignKey | Sí | No | NULL | Usuario que realizó el borrado |
| `history` | HistoricalRecords | - | - | - | Auditoría de cambios |

**Constraint Especial:**
```sql
UNIQUE (user_id) WHERE is_main=TRUE AND is_active=TRUE
-- Solo una dirección principal activa por usuario
```

**Métodos:**

```python
def reassign_main_address():
    """Si se borra la dirección principal, asigna otra como principal"""
    
def soft_delete(actor=None):
    """Borrado lógico de dirección"""
    
def delete(using=None, keep_parents=False):
    """Override para usar soft_delete"""
```

**Índices:**
```sql
CREATE INDEX idx_address_user ON users_address(user_id);
CREATE INDEX idx_address_main ON users_address(user_id, is_main) WHERE is_active=TRUE;
```

---

### Model: Region

**Descripción**: Región de Chile.

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | AutoField | ID |
| `name` | CharField | Nombre de región (Ej: "Región de Antofagasta") |

**Datos**: 15 regiones de Chile (desde Arica a Magallanes)

---

### Model: Commune

**Descripción**: Comuna de Chile (pertenece a una Región).

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | AutoField | ID |
| `region_id` | ForeignKey | Región a la que pertenece |
| `name` | CharField | Nombre de comuna (Ej: "Santiago") |

**Datos**: ~346 comunas de Chile

---

## 🛍️ Products Service Data Models

### Model: Product

**Descripción**: Producto del catálogo de GuitarZone.

**Campos:**

| Campo | Tipo | Nulo | Default | Descripción |
|-------|------|------|---------|-------------|
| `id` | AutoField | No | Auto | Identificador único |
| `name` | CharField | No | - | Nombre del producto (máx 50 chars) |
| `description` | TextField | No | - | Descripción detallada del producto |
| `price` | DecimalField | No | - | Precio en CLP (máx 10 dígitos, 2 decimales) |
| `stock` | PositiveBigIntegerField | No | 0 | Cantidad disponible |
| `category_id` | ForeignKey | Sí | NULL | Categoría del producto |
| `measure_unit_id` | ForeignKey | Sí | NULL | Unidad de medida |
| `image` | ImageField | Sí | NULL | Imagen del producto (upload_to='products/') |
| `created_at` | DateTimeField | No | NOW() | Fecha de creación |
| `updated_at` | DateTimeField | No | NOW() | Fecha de última actualización |
| `state` | BooleanField | No | True | Flag de producto activo (borrado lógico) |
| `created_by_id` | IntegerField | Sí | NULL | ID del usuario que creó |
| `updated_by_id` | IntegerField | Sí | NULL | ID del usuario que actualizó |
| `history` | HistoricalRecords | - | - | Auditoría de cambios |

**Métodos:**

```python
def __str__(self):
    return self.name
```

**Índices:**
```sql
CREATE INDEX idx_product_category ON products_product(category_id);
CREATE INDEX idx_product_state ON products_product(state);
CREATE INDEX idx_product_stock ON products_product(stock);
```

---

### Model: Category

**Descripción**: Categoría de productos.

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | AutoField | ID |
| `name` | CharField | Nombre de categoría (Ej: "Guitarras Acústicas") |
| `created_at` | DateTimeField | Fecha de creación |
| `updated_at` | DateTimeField | Última actualización |
| `state` | BooleanField | Activo (borrado lógico) |
| `created_by_id` | IntegerField | Usuario que creó |
| `updated_by_id` | IntegerField | Usuario que actualizó |
| `history` | HistoricalRecords | Auditoría |

**Ejemplos de categorías:**
- Guitarras Acústicas
- Guitarras Eléctricas
- Bajos
- Amplificadores
- Pedales de Efectos
- Accesorios
- Cuerdas
- Capos y Afinadores

---

### Model: MeasureUnit

**Descripción**: Unidad de medida de productos.

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | AutoField | ID |
| `name` | CharField | Nombre de unidad (Ej: "Unidad", "Paquete") |
| `created_at` | DateTimeField | Fecha de creación |
| `updated_at` | DateTimeField | Última actualización |
| `state` | BooleanField | Activo |
| `created_by_id` | IntegerField | Usuario que creó |
| `updated_by_id` | IntegerField | Usuario que actualizó |
| `history` | HistoricalRecords | Auditoría |

**Ejemplos:**
- Unidad
- Paquete x2
- Paquete x6
- Set completo
- Docena

---

## 📦 Orders Service Data Models

### Model: Order

**Descripción**: Orden de compra realizada por un usuario.

**Campos:**

| Campo | Tipo | Nulo | Default | Descripción |
|-------|------|------|---------|-------------|
| `id` | AutoField | No | Auto | Identificador único |
| `user_id` | IntegerField | No | - | ID del usuario (no FK para independencia de DBs) |
| `status` | CharField | No | PENDING | Estado de la orden (PENDING, PAID, CANCELLED) |
| `total_amount` | DecimalField | No | - | Total en CLP (entero, 8 dígitos) |
| `user_address` | IntegerField | Sí | NULL | ID de la dirección de envío |
| `created_at` | DateTimeField | No | NOW() | Fecha de creación |
| `updated_at` | DateTimeField | No | NOW() | Última actualización |
| `state` | BooleanField | No | True | Flag de orden activa |
| `created_by_id` | IntegerField | Sí | NULL | Usuario que creó |
| `updated_by_id` | IntegerField | Sí | NULL | Usuario que actualizó |
| `history` | HistoricalRecords | - | - | Auditoría |

**Estados (TextChoices):**

```python
PENDING = 'PENDING'      # Esperando pago
PAID = 'PAID'            # Pagado
CANCELLED = 'CANCELLED'  # Cancelada (stock liberado)
```

**Índices:**
```sql
CREATE INDEX idx_order_user_id ON orders_order(user_id);
CREATE INDEX idx_order_status ON orders_order(status);
```

---

### Model: OrderDetail

**Descripción**: Items (productos) dentro de una orden.

**Campos:**

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| `id` | AutoField | No | Identificador único |
| `product_id` | IntegerField | No | ID del producto (no FK para independencia) |
| `product_title` | CharField | Sí | Nombre del producto (snapshot al momento de compra) |
| `quantity` | IntegerField | No | Cantidad comprada |
| `unit_price` | DecimalField | No | Precio unitario (snapshot al momento) |
| `image_url` | URLField | Sí | URL de imagen del producto (snapshot) |
| `order_id` | ForeignKey | No | Referencia a Order |
| `history` | HistoricalRecords | - | Auditoría |

**Índices:**
```sql
CREATE INDEX idx_orderdetail_order ON orders_orderdetail(order_id);
```

**Nota**: Usa campos `*_id` e IDs en lugar de ForeignKeys para mantener independencia entre microservicios.

---

## 📤 Serializers

### Users Service Serializers

**UserSerializer** (Lectura)
```python
{
    "id": 1,
    "email": "user@guitarzone.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "912345678",
    "is_verified": true,
    "is_active": true,
    "is_staff": false,
    "date_joined": "2024-01-15T10:30:00Z",
    "is_profile_complete": true
}
```

**UserCreateSerializer** (Registro)
```python
{
    "email": "newuser@guitarzone.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez"
}
```

**UserUpdateSerializer** (Actualización de perfil)
```python
{
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "987654321"
}
```

**AddressSerializer**
```python
{
    "id": 1,
    "user": 1,
    "commune": {
        "id": 1,
        "name": "Santiago",
        "region": 1
    },
    "street": "Avenida Principal",
    "number": "123",
    "apartment": "A",
    "is_main": true,
    "is_active": true
}
```

**TokenLoginSerializer**
```python
{
    "email": "user@guitarzone.com",
    "password": "SecurePass123!"
}
```

**Token Response**
```python
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUz...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUz..."
}
```

---

### Products Service Serializers

**ProductSerializer**
```python
{
    "id": 1,
    "name": "Guitarra Acústica Premium",
    "description": "Guitarra acústica de madera maciza, sonido profesional",
    "price": "199999.99",
    "stock": 5,
    "category": {
        "id": 1,
        "name": "Guitarras Acústicas"
    },
    "measure_unit": {
        "id": 1,
        "name": "Unidad"
    },
    "image": "https://api.guitarzone.cl/media/products/guitar_1.jpg",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-16T14:20:00Z",
    "state": true
}
```

**CategorySerializer**
```python
{
    "id": 1,
    "name": "Guitarras Acústicas"
}
```

**MeasureUnitSerializer**
```python
{
    "id": 1,
    "name": "Unidad"
}
```

---

### Orders Service Serializers

**OrderSerializer**
```python
{
    "id": 123,
    "user_id": 5,
    "status": "PENDING",
    "total_amount": 450000,
    "user_address": 1,
    "created_at": "2024-01-20T15:30:00Z",
    "updated_at": "2024-01-20T15:30:00Z",
    "order_items": [
        {
            "id": 1,
            "product_id": 1,
            "product_title": "Guitarra Acústica Premium",
            "quantity": 2,
            "unit_price": 199999.99,
            "image_url": "https://api..."
        },
        {
            "id": 2,
            "product_id": 3,
            "product_title": "Cuerdas de Guitarra x6",
            "quantity": 1,
            "unit_price": 50000.00,
            "image_url": "https://api..."
        }
    ]
}
```

**OrderCreateSerializer**
```python
{
    "order_items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 3, "quantity": 1}
    ]
}
```

**OrderItemDetailSerializer**
```python
{
    "product_id": 1,
    "product_title": "Guitarra Acústica",
    "quantity": 2,
    "unit_price": 199999.99,
    "image_url": "..."
}
```

---

## 🔗 Relaciones entre Modelos

### Diagrama ER

```
USERS SERVICE
┌─────────────────────────────────┐
│         User                    │
├─────────────────────────────────┤
│ id (PK)                         │
│ email (UNIQUE)                  │
│ password                        │
│ first_name                      │
│ last_name                       │
│ phone (UNIQUE)                  │
│ is_verified                     │
│ is_active                       │
│ deleted_by_id (FK self)         │
└────────────┬────────────────────┘
             │
             │ 1:N
             │
      ┌──────▼─────────────────┐
      │     Address            │
      ├──────────────────────┤
      │ id (PK)              │
      │ user_id (FK) ────────┤
      │ commune_id (FK) ──┐  │
      │ street           │  │
      │ number           │  │
      │ apartment        │  │
      │ is_main          │  │
      │ deleted_by_id(FK)│  │
      └──────────────────┘  │
                            │
                      ┌─────▼──────────┐
                      │   Commune      │
                      ├────────────────┤
                      │ id (PK)        │
                      │ region_id (FK) │
                      │ name           │
                      └────────────────┘


PRODUCTS SERVICE
┌──────────────────────────┐
│     Category             │
├──────────────────────────┤
│ id (PK)                  │
│ name                     │
└──────────────┬───────────┘
               │
               │ 1:N
               │
    ┌──────────▼──────────────────┐
    │     Product                │
    ├──────────────────────────┤
    │ id (PK)                │
    │ name                  │
    │ description          │
    │ price               │
    │ stock              │
    │ category_id(FK) ───┘
    │ measure_unit_id(FK)─────────┐
    │ image                       │
    │ created_at                  │
    │ updated_at                  │
    └─────────────────────────────┘
                                  │
                    ┌─────────────▼──────────┐
                    │  MeasureUnit          │
                    ├──────────────────────┤
                    │ id (PK)              │
                    │ name                 │
                    └──────────────────────┘


ORDERS SERVICE
┌────────────────────────────┐
│      Order                 │
├────────────────────────────┤
│ id (PK)                    │
│ user_id (INT - no FK)      │
│ status                     │
│ total_amount               │
│ user_address (INT - no FK) │
│ created_at                 │
│ updated_at                 │
└────────────┬───────────────┘
             │
             │ 1:N
             │
      ┌──────▼──────────────┐
      │   OrderDetail      │
      ├────────────────────┤
      │ id (PK)            │
      │ order_id (FK) ─────┤
      │ product_id (INT)   │
      │ quantity           │
      │ unit_price         │
      │ image_url          │
      └────────────────────┘
```

---

## ⚙️ Valores por Defecto y Validaciones

### User Validations

```python
# Email
- Debe ser único
- Formato válido de email
- No puede ser vacío

# Password
- Mínimo 8 caracteres
- Al menos 1 mayúscula
- Al menos 1 minúscula
- Al menos 1 número
- Al menos 1 carácter especial

# Phone
- 9 dígitos (formato +56 9 XXXX XXXX)
- Debe ser único
- Solo números

# First/Last Name
- Máximo 100 caracteres
- No requerido pero recomendado
```

### Product Validations

```python
# Name
- Máximo 50 caracteres
- No puede ser vacío

# Price
- Decimal positivo
- Máximo 8 dígitos enteros
- Máximo 2 decimales
- No puede ser 0 o negativo

# Stock
- Entero positivo o 0
- Máximo valor: 9223372036854775807 (BigInt)

# Image
- Formatos: JPG, PNG, GIF, WEBP
- Máximo 5MB
- Se almacena en: media/products/

# Category & MeasureUnit
- Opcionales pero recomendados
```

### Order Validations

```python
# order_items
- Debe tener al menos 1 item
- product_id debe existir en Products Service
- quantity debe ser > 0
- Stock debe ser suficiente

# user_address (opcional al crear)
- Si se proporciona, debe pertenencer al usuario
- No es requerido en POST inicial

# total_amount
- Calculado automáticamente
- No se puede enviar manualmente
```

---

## 🔐 Permisos por Operación

| Operación | Permiso Requerido | Notas |
|-----------|------------------|-------|
| Registrar usuario | AllowAny | Cualquiera puede registrarse |
| Login | AllowAny | Cualquiera puede intentar login |
| Ver perfil propio | IsAuthenticated | Solo el usuario autenticado |
| Actualizar perfil | IsAuthenticated | Solo el usuario autenticado |
| Listar productos | AllowAny | Acceso público al catálogo |
| Ver detalle producto | AllowAny | Acceso público |
| Crear producto | IsStaff | Solo administradores |
| Editar producto | IsStaff | Solo administradores |
| Eliminar producto | IsStaff | Solo administradores (soft delete) |
| Crear orden | IsAuthenticated | Usuario verificado |
| Ver orden propia | IsAuthenticated | Solo el dueño de la orden |
| Pagar orden | IsAuthenticated | Solo el dueño |
| Webhook MP | AllowAny | Verificación por X-Signature |
| Reservar stock | IsInternalService | Solo desde servicios autorizados |
| Liberar stock | IsInternalService | Solo desde servicios autorizados |

---

## 📊 Query Patterns Comunes

### Get User with Addresses
```python
user = User.objects.prefetch_related('addresses').get(email='user@guitarzone.com')
user.addresses.all()  # No hace query adicional
```

### Get Products with Category
```python
products = Product.objects.select_related('category', 'measure_unit')\
    .filter(state=True, stock__gt=0)
```

### Get Order with Details
```python
order = Order.objects.prefetch_related('order_items').get(id=123)
for item in order.order_items.all():  # No hace queries adicionales
    print(item.product_title, item.quantity)
```

### Get Order History
```python
from simple_history.models import HistoricalOrder
history = HistoricalOrder.objects.filter(id=123).order_by('history_date')
```

---

**Última actualización:** Abril 2026
