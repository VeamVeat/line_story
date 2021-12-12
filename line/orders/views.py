# from django.core.serializers import json
import json

from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.db.models import F

from orders.models import CartItem, Order
from products.models import Product, ProductFile
from orders.forms import OrderForm
from users.models import Wallet


class CartView(ListView):
    model = CartItem
    template_name = 'orders/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        queryset = self.get_queryset()
        cart_all = queryset.filter(user=self.request.user)
        context['products_all'] = cart_all
        return context


class DeleteProduct(View):
    model = CartItem
    template_name = 'orders/cart.html'

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_in_cart = get_object_or_404(self.model, user=request.user, product_id=product_id)
        # что возвращает get_object_or_404
        product_in_cart.delete()
        return redirect('orders:cart')


class CheckoutView(View):
    model = CartItem
    template_name = 'orders/checkout.html'

    def get(self, request, *args, **kwargs):

        cart_item_current_user = self.model.objects.filter(user=request.user)
        total_price_and_total_count = cart_item_current_user.aggregate(total_price=models.Sum(F('product__price')
                                                                                              * F('quantity')),
                                                                       total_count=models.Count('product__id'))
        total_price_product = total_price_and_total_count['total_price']
        total_count_product = total_price_and_total_count['total_count']

        form = OrderForm()
        #колличество добавленного товара привышает колличество имеющегося на складе
        product_all = []
        for products in cart_item_current_user:
            current_product_image = ProductFile.objects.filter(product_id=products.product.id).first()
            product = {
                "id": products.product.id,
                "type": products.product.type.name,
                "title": products.product.title,
                "description": products.product.description,
                "price": float(products.product.price),
                "year": products.product.year,
                "image": current_product_image.image.url,
                'quantity': products.quantity
            }
            product_all.append(product)
        context = {'products': product_all, 'total_price': float(total_price_product),
                   'total_count': total_count_product, 'form': form}

        Order.objects.create(
            user=request.user,
            quantity=total_count_product,
            final_price=total_price_product,
            product_list={'products': product_all}
        )

        return render(request, self.template_name, context)


class MakeOrderView(View):
    model = Order

    def post(self, request, *args, **kwargs):

        form = OrderForm(request.POST or None)
        if form.is_valid():
            address = form.cleaned_data.get('address')

            order_user = self.model.objects.get(user=request.user, is_active=True)
            money = Wallet.objects.get(user=request.user)

            if order_user.final_price > money.ballance:
                self.model.objects.get(user=request.user, is_active=True).delete()
                redirect('home')
            else:
                request.user.diminish_balance(order_user.final_price)
                order_user.address = address
                order_user.is_active = False
                order_user.save(update_fields=['address', 'is_active'])

                subject = 'your order has been completed'
                message = render_to_string('orders/new_order_notification.html', {
                    'user': request.user,
                    'count': order_user.quantity,
                    'price': order_user.final_price
                })
                request.user.email_user(subject, message)

                CartItem.objects.filter(user=request.user).delete()
            return redirect('home')
        return HttpResponseRedirect('orders:checkout')

#HttpResponseRedirect / redirect