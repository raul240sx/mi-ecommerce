import mercadopago

from django.conf import settings

from apps.orders.models.order import Order
from apps.base.exceptions import PaymentError



class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    
    def create_payment_preference(self, order):
        frontend_url = settings.FRONTEND_URL
        api_url = f'https://{settings.DOMAIN_NAME}'


        if order.status == Order.Status.PENDING:

            order_items = order.order_items.all()

            items_list = []

            for item in order_items:
                new_item = {
                    'title':item.product_title,
                    'quantity':item.quantity,
                    'unit_price':int(item.unit_price),
                    'currency_id':'CLP'
                }

                items_list.append(new_item)


            preference_data = {
                'items':items_list,
                'auto_return':'approved',
                'back_urls':{
                    'success':f'{frontend_url}/success/',
                    'failure':f'{frontend_url}/failure/',
                    'pending':f'{frontend_url}/pending/'
                },
                'external_reference':str(order.id),
                'notification_url':f'{api_url}/orders-api/webhook/'
            }

            preference_response = self.sdk.preference().create(preference_data)

            return preference_response.get('response')


        elif order.status != Order.Status.PENDING:
            raise PaymentError(f'La orden nro. {order.id} se encuentra en estado {order.status}. Proceso de pago inválido')




    def get_payment_info(self, payment_id):
        
        return self.sdk.payment().get(str(payment_id))



