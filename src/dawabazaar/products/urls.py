from django.urls import path
from .views import create_product, product_list, edit_product, delete_product, category_base_view, product_details

app_name = "products"
urlpatterns = [
    path("create/", create_product, name="create-product"),
    path("list_all/", product_list, name="listall-products"),
    path("<int:pk>/edit/", edit_product, name="edit-product"),
    path("<int:pk>/delete/", delete_product, name="delete-product"),
    path('details/<slug:slug>/', product_details, name='product-detail'),
    path("category/<str:category_name>/", category_base_view, name="display-product")
]


