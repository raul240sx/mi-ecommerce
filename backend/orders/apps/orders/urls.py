from django.urls import path

from apps.orders.views import OrderCreateView, MpWebhookView, OrderView, MpPaymentView

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('order-retrieve/<int:id>/', OrderView.as_view(), name='order-retrieve'),
    path('order-payment/<int:id>/', MpPaymentView.as_view(), name='order-payment'),
    path('webhook/', MpWebhookView.as_view(), name='webhook'),
]
