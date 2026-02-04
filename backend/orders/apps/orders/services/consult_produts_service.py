import requests

from django.conf import settings
from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.orders.models import Order, OrderDetail




products_url = settings.PRODUCTS_SERVICE_URL
internal_key = settings.INTERNAL_SERVICE_KEY



def validate_item_list(expected_items, recieved_items):

    for item in expected_items:
        if recieved_items.get(str(item)) is None:
            raise ValidationError(f'No se ha encontrado el producto id {item}')
    



def validate_stock_items(expected_items, recieved_items):

    total_amount = 0

    validated_order_items = {}
    
    for item in expected_items:
        recieved_item = recieved_items.get(str(item['product_id']))

        if item['quantity'] > recieved_item['stock']:
            raise ValidationError(f'Stock insuficiente del producto id {item['product_id']}')
        
        total_amount += (recieved_item['price'] * item['quantity']) 

        new_item = {
            'product_id':item['product_id'],
            'quantity':item['quantity'],
            'unit_price':recieved_item['price']
        }

        validated_order_items[item['product_id']] = new_item
    
    return total_amount, validated_order_items




def create_order_and_detail(user_id, total_amount, validated_order_items):

    with transaction.atomic():

        order = Order.objects.create(user_id=user_id, total_amount=total_amount)

        details = []

        for item in validated_order_items.values():

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
        'X-Internal_Service-Key':internal_key,
        'Content-Type':'application/json'
    }

    items_id = []

    products_url

    for item in order_items:
        items_id.append(item['product_id'])

    query_params = {'ids':','.join(map(str, items_id))}
 

    try:
        request = requests.get(url=products_url, params=query_params, headers=header, timeout=5)

        if request.status_code == 200:
            items_info = request.json()
            
            validate_item_list(items_id, items_info)

            total_amount, validated_order_items = validate_stock_items(order_items, items_info)


            order = create_order_and_detail(user_id, total_amount, validated_order_items)

            return order
        
        else:
            raise ValidationError('Fallo en peticion HTTP')
        
    except requests.exceptions.RequestException as e:
        raise ValidationError('Error de conexión con el servicio de products-service')
    