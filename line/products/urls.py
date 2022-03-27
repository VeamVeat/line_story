from django.urls import path

from products.views import ProductView, ShowProductView, SearchResultsView,\
    AddProduct, FilterProductView, MakeReservation

app_name = "products"

urlpatterns = [
    path("products/", ProductView.as_view(), name="products_all"),
    path('reserve_product/', MakeReservation.as_view(), name='reserve_product'),

    path("filter/", FilterProductView.as_view(), name="filter"),
    path('search/', SearchResultsView.as_view(), name='search'),

    path("products/<slug:product_slug>", ShowProductView.as_view(), name="product"),

    path('add-to-cart/', AddProduct.as_view(), name='add_to_cart')
]
