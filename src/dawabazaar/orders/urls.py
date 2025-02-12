from django.urls import path
from .views import order_list, update_order_status

app_name = 'orders'
urlpatterns = [
    path('order_list/', order_list, name='order-list'),
    path('update_order_status/<int:pk>/',update_order_status, name="update-order-status")
]
