import mercadopago

from django.conf import settings



ngrok_url = settings.NGROK_URL


class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    
    def create_payment_preference(self, order):

        order_items = order.order_items.all()

        items_list = []

        for item in order_items:
            new_item = {
                'title':item.product_title,
                'quantity':item.quantity,
                'unit_price':float(item.unit_price),
                'currency_id':'CLP'
            }

            items_list.append(new_item)


        preference_data = {
            'items':items_list,
            'auto_return':'approved',
            'back_urls':{
                'success':f'{ngrok_url}/success',
                'failure':f'{ngrok_url}/failure',
                'pending':f'{ngrok_url}/pending'
            },
            'external_reference':str(order.id),
            'notification_url':f'{ngrok_url}/orders-api/webhook'
        }

        preference_response = self.sdk.preference().create(preference_data)

        return preference_response.get('response')




