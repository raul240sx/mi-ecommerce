import requests

from decimal import Decimal

from django.conf import settings
from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.orders.models import Order, OrderDetail
from apps.orders.tasks.release_stock_task import release_stock_task




products_url = settings.PRODUCTS_SERVICE_URL
internal_key = settings.INTERNAL_SERVICE_KEY
release_stock_url = settings.PRODUCTS_RELEASE_STOCK



def amount_and_item_info(expected_items, received_items):

    total_amount = Decimal('0')

    order_items_info = {}
    
    for item in expected_items:
        received_item = received_items.get(str(item['product_id']))

        if received_item is None:
            raise ValidationError('Producto del diccionario "received_items" faltante')
        

        price = Decimal(received_item['price'])
        total_amount += (price * item['quantity']) 

        new_item = {
            'product_id':item['product_id'],
            'quantity':item['quantity'],
            'unit_price':price
        }

        order_items_info[item['product_id']] = new_item
    
    return total_amount, order_items_info




def create_order_and_detail(user_id, total_amount, order_items_info):

    with transaction.atomic():

        order = Order.objects.create(user_id=user_id, total_amount=total_amount)

        details = []

        for item in order_items_info.values():

            new_detail = OrderDetail(
                product_id = item['product_id'],
                quantity = item['quantity'],
                unit_price = item['unit_price'],
                order = order
            )

            details.append(new_detail)

        OrderDetail.objects.bulk_create(details)

        return order



def validate_and_get_products_info(order_items, user_id):

    header = {
        'Internal-Service-Key':internal_key,
        'Content-Type':'application/json'
    }

    payload = {'items':order_items}

    try:
        response = requests.post(url=products_url, json=payload, headers=header, timeout=5)

        if response.status_code == 200:

            items_info = response.json()
            total_amount, order_items_info = amount_and_item_info(order_items, items_info)


            try:
                order = create_order_and_detail(user_id, total_amount, order_items_info)
                release_stock_task.apply_async(args=[order.id], countdown=10)

                return order


            except Exception as e:

                requests.post(url=release_stock_url, json=payload, headers=header, timeout=5)

                raise ValidationError('La orden no pudo ser procesada. El stock ha sido liberado.')

        else:
            try:
                error_data = response.json()
                detail = error_data.get('detail')

                if isinstance(detail, list):
                    error_msg = ', '.join([f'{d}' for d in detail])
                elif detail is None:
                    error_msg = error_data.get('message') or 'Error no especificado en el servicio de products-service'
                else:
                    error_msg = str(detail)

            except Exception:
                error_msg = f'El servicio de productos devolvió un error inesperado (Status {response.status_code})'

            raise ValidationError(error_msg)
        
    except requests.exceptions.RequestException as e:
        raise ValidationError('Error de conexión con el servicio de products-service')
    