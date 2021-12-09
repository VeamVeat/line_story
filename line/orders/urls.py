from django.urls import path
from orders.views import CartView,  DeleteProduct, CheckoutView, MakeOrderView

app_name = "orders"

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path('delete-product/<int:product_id>/', DeleteProduct.as_view(), name='delete_product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order')
]
