import requests

from django.conf import settings

from rest_framework.exceptions import ValidationError




products_url = settings.PRODUCTS_SERVICE_URL
internal_key = settings.INTERNAL_SERVICE_KEY



def validate_item_list(expected_items, recieved_items):

    for item in expected_items:
        if recieved_items.get(str(item)) is None:
            raise ValidationError(f'No se ha encontrado el producto id {item}')
    



def validate_stock_items(expected_items, recieved_items):

    total_amount = 0
    
    for item in expected_items:
        recieved_item = recieved_items.get(str(item['product_id']))

        if item['quantity'] > recieved_item['stock']:
            raise ValidationError(f'Stock insuficiente del producto id {item['product_id']}')
        
        total_amount += (recieved_item['price'] * item['quantity']) 
    
    return total_amount



def validate_and_get_products_info(validated_order_items:list):

    header = {
        'X-Internal_Service-Key':internal_key,
        'Content-Type':'application/json'
    }

    items_id = []

    products_url

    for item in validated_order_items:
        items_id.append(item['product_id'])

    query_params = {'ids':','.join(map(str, items_id))}
 

    try:
        request = requests.get(url=products_url, params=query_params, headers=header, timeout=5)

        if request.status_code == 200:
            items_info = request.json()
            
            validate_item_list(items_id, items_info)

            total_amount = validate_stock_items(validated_order_items, items_info)



            return {
                'products_detail':items_info,
                'total_amount':total_amount
                }

        
        else:
            raise ValidationError('Fallo en peticion HTTP')
        
    except requests.exceptions.RequestException as e:
        raise ValidationError('Error de conexión con el servicio de products-service')
    