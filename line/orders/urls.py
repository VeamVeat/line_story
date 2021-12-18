from django.urls import path

from orders.views import DeleteReservationProduct, ReservationView
from orders.views import CartView, DeleteProduct, CheckoutView,\
    MakeOrderView, OrderView, NotMoneyView, DiminishProductView, IncreaseProductView

app_name = "orders"

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("all-orders/", OrderView.as_view(), name="all_orders"),
    path('diminish_product/<int:product_id>/', DiminishProductView.as_view(), name='diminish_product'),
    path('increase_product/<int:product_id>/', IncreaseProductView.as_view(), name='increase_product'),
    path('delete-product/<int:product_id>/', DeleteProduct.as_view(), name='delete_product'),

    path("reserved-products/", ReservationView.as_view(), name="reserved_products"),
    path("deleting-reserved-product/<int:product_id>/", DeleteReservationProduct.as_view(), name="deleting_reserved"),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('not-money/', NotMoneyView.as_view(), name='not_money')
]
