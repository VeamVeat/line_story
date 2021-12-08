from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, get_object_or_404

from orders.models import Cart
from products.models import Product


class CartView(ListView):
    model = Cart
    template_name = 'orders/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        queryset = self.get_queryset()
        cart_all = queryset.filter(user=self.request.user)
        context['products_all'] = cart_all
        return context


class DeleteProduct(View):
    model = Cart
    template_name = 'orders/cart.html'

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_in_cart = get_object_or_404(self.model, user=request.user, product_id=product_id)
        product_in_cart.delete()
        return redirect('orders:cart')
