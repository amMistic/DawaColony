from django.urls import path
from .views import create_product, product_list, edit_product, delete_product

app_name = "products"
urlpatterns = [
    path("create/", create_product, name="create-product"),
    path("list_all/", product_list, name="listall-products"),
    path("<int:pk>/edit/", product_list, name="edit-product"),
    path("<int:pk>/delete/", product_list, name="delete-product"),
]
