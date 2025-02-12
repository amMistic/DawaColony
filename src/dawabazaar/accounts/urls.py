from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    seller_register_view,
    customer_register_view,
    login_user_view,
    logout_view
)
app_name = 'accounts'

urlpatterns = [
    path('login/', login_user_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', customer_register_view, name='register'),
    path('become-seller/', seller_register_view, name='become-seller'),
]