from django.urls import path
from products.views import ProductView, ShowProductView, SearchResultsView

app_name = "products"

urlpatterns = [
    path("products/", ProductView.as_view(), name="product_all"),
    path("products/<slug:product_slug>", ShowProductView.as_view(), name="product"),
    path('search/', SearchResultsView.as_view(), name='search'),
]


