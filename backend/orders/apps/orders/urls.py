from django.urls import path

from apps.orders.views import OrderCreateView, MpWebhookView, OrderView

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('order-retrieve/<int:id>/', OrderView.as_view(), name='order-retrieve'),
    path('webhook/', MpWebhookView.as_view(), name='webhook'),

]
