from django.urls import path
from orders.views import CartView,  DeleteProduct

app_name = "orders"

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path('delete-product/<int:product_id>/', DeleteProduct.as_view(), name='delete_product')
]
