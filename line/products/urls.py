from django.urls import path
from products.views import ProductView, ShowProductView, SearchResultsView, AddProduct, FilterProductView

app_name = "products"

urlpatterns = [
    path("filter/", FilterProductView.as_view(), name="filter"),
    path("products/", ProductView.as_view(), name="products_all"),
    path("products/<slug:product_slug>", ShowProductView.as_view(), name="product"),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('add-to-cart/<int:product_id>/', AddProduct.as_view(), name='add_to_cart')
]


