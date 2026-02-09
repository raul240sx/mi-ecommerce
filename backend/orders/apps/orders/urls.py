from django.urls import path

from apps.orders.views import OrderCreateView, MpWebhookView

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('webhook/', MpWebhookView.as_view(), name='webhook'),

]
