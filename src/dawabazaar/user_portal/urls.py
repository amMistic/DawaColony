from django.urls import path

from .views import (
    profile,
    update_profile,
    manage_addresses,
    add_address,
    edit_address,
    delete_address,
    set_default_address,
    change_password
)

app_name = "customer"
urlpatterns = [
    path("profile/", profile, name="user-profile"),
    path("profile/<int:id>/update/", update_profile, name="update-user-profile"),
    path('change-password/', change_password, name='change-password'),
    path("addresses/", manage_addresses, name="manage-user-addresses"),
    path("addresses/add/", add_address, name="add-address"),
    path("addresses/edit/<int:address_id>/", edit_address, name="edit-address"),
    path("addresses/delete/<int:address_id>/", delete_address, name="delete-address"),
    path("addresses/set-default/<int:address_id>/", set_default_address, name="set-default-address"),
]
