from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

from products.models import ProductFile, Product, ProductType
from products.services import ProductServices


class TypeYearsProduct:
    def get_type(self):
        return ProductType.objects.all()

    def get_years(self):
        return Product.objects.all().values("year").distinct()


class DeleteProductFile(DeleteView):
    model = ProductFile
    permission_required = ['change_profile']

    def get_success_url(self):
        product_id = self.kwargs['product_id']
        return reverse('admin:products_product_change', kwargs={'object_id': product_id})


class ProductView(TypeYearsProduct, ListView):
    model = Product
    template_name = 'products/products_all.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        product_services = ProductServices(user=self.request.user,
                                           model=Product)

        contex['all_product_in_cart'] = product_services.get_all_product_id_in_cart()

        return contex


class ShowProductView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'detail_product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['title'] = 'detail product'

        product_services = ProductServices(user=self.request.user,
                                           model=self.model,
                                           odject_id=self.object.id)

        contex['all_product_in_cart'] = product_services.get_all_product_id_in_cart()
        contex['all_photo_product'] = product_services.get_all_product_photo()
        return contex


class SearchResultsView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'search_products'

    def get_queryset(self):
        queryset = super().get_queryset()

        text_search = self.request.GET.get('search')
        if text_search:
            queryset = queryset.filter(Q(title__icontains=text_search) |
                                       Q(type__name__icontains=text_search))
        return queryset


class AddProduct(View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_services = ProductServices(user=self.request.user,
                                           model=Product,
                                           product_id=product_id)

        object_cart, create_cart = product_services.get_or_create_cart_item()
        if not create_cart:
            object_cart.quantity += 1
            object_cart.save()

        return redirect('orders:cart')


class FilterMoviesView(TypeYearsProduct, ListView):
    model = Product
    template_name = 'products/products_all.html'
    context_object_name = 'products'

    def get_queryset(self):

        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(type__name__in=self.request.GET.getlist("type"))
        )
        return queryset
