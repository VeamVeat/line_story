from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

from products.models import ProductFile, Product


class DeleteProductFile(DeleteView):
    model = ProductFile
    permission_required = ['change_profile']

    def get_success_url(self):
        product_id = self.kwargs['product_id']
        return reverse('admin:products_product_change', kwargs={'object_id': product_id})


class ProductView(ListView):
    # queryset
    model = Product
    template_name = 'products/products_all.html'
    context_object_name = 'products'


class ShowProductView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'detail_product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['title'] = 'detail product'
        current_product = self.model.objects.get(id=self.object.id)
        contex['all_photo_product'] = current_product.product_file.all()
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
