import requests

from django.conf import settings

from celery import shared_task

from apps.orders.models.order import Order



internal_key = settings.INTERNAL_SERVICE_KEY
release_stock_url = settings.PRODUCTS_RELEASE_STOCK

@shared_task(bind=True, autoretry_for=(requests.exceptions.RequestException,), retry_backoff=True, max_retries=3)
def release_stock_task(self, order_id):

    order = Order.objects.filter(id=order_id, state=True).first()

    if order is None:
        return f'Orden {order_id} no encontrada'
    

    order_items = order.order_items.all()
    
    if not order_items.exists():
         return f'Orden {order_id} no contiene productos'

    items = []
    if order.status != 'PENDING':
        return f'Orden {order_id} ya no se encuentra en estado "Pendiente", estado actual: {order.status}'

    for item in order_items:
        items.append({'product_id':item.product_id, 'quantity':item.quantity})

    header = {
        'Internal-Service-Key':internal_key,
        'Content-Type':'application/json'
    }

    payload = {'items':items}

    response = requests.post(release_stock_url, json=payload, headers=header, timeout=5)

    if response.status_code == 200:
        order.status = Order.Status.CANCELLED
        order.save()
        return f'Stock de productos de la orden {order_id} liberado satisfactoriamente'

    else:
        raise requests.exceptions.RequestException(f'Error de conexión con el servicio de products-service:{response.status_code}')
        