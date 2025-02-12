from django.urls import path
from .views import dashboard, seller_profile, update_seller_profile, change_password

app_name = 'seller'
urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('profile/',seller_profile, name="user-profile"),
    path('profile/<int:id>/edit', update_seller_profile, name="update-seller-profile"),
    path('profile/update-password/',change_password, name='change-password')
]