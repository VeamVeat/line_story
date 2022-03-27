import json

from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render
from django.http import JsonResponse

from orders.models import CartItem, Order, Reservation
from orders.forms import OrderForm
from orders.services import OrderServices, CartItemServices, ReservationServices
from products.views import is_ajax
from products.models import Product


class CartView(ListView):
    model = CartItem
    template_name = 'orders/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        queryset = self.get_queryset()
        form = OrderForm()
        cart_item_all = queryset.filter(user=self.request.user)

        cart_item_services = CartItemServices(user=self.request.user, model=self.model)

        total_price = cart_item_services.get_total_price()
        total_count = cart_item_services.get_total_count()

        context['form'] = form
        context['products_all'] = cart_item_all
        context['total_price_product'] = total_price
        context['total_count_product'] = total_count
        return context


class DeleteProduct(View):
    model = CartItem
    template_name = 'orders/cart.html'

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        cart_item_services = CartItemServices(user=self.request.user,
                                              model=self.model,
                                              product_id=product_id)
        cart_item_services.delete_product()
        return redirect('orders:cart')


class DiminishProductView(View):
    model = CartItem

    def post(self, request, *args, **kwargs):

        if is_ajax(request=request):
            data = json.load(request)
            product_id = data.get('product_id')
            product_price = Product.objects.get(id=product_id).price

            cart_item_services = CartItemServices(user=self.request.user,
                                                  model=self.model,
                                                  product_id=product_id)

            calculate_product_success = cart_item_services.calculate_product(param='diminish')
            product_in_cart_quantity = cart_item_services.get_quantity_product_in_cart()
            total_price_all_cart = cart_item_services.get_total_price()
            total_count_all_cart = cart_item_services.get_total_count()

            assert calculate_product_success

            data_message = {'product_price': float(product_price),
                            'product_in_cart_quantity': product_in_cart_quantity,
                            'total_price_all_cart': total_price_all_cart,
                            'total_count_all_cart': total_count_all_cart}

            return JsonResponse(data_message)


class IncreaseProductView(View):
    model = CartItem

    def post(self, request):
        if is_ajax(request=request):
            data = json.load(request)
            product_id = data.get('product_id')
            product_price = Product.objects.get(id=product_id).price

            cart_item_services = CartItemServices(user=self.request.user,
                                                  model=self.model,
                                                  product_id=product_id)

            calculate_product_success = cart_item_services.calculate_product(param='increase')
            product_in_cart_quantity = cart_item_services.get_quantity_product_in_cart()
            total_price_all_cart = cart_item_services.get_total_price()
            total_count_all_cart = cart_item_services.get_total_count()

            assert calculate_product_success

            data_message = {'product_price': float(product_price),
                            'product_in_cart_quantity': product_in_cart_quantity,
                            'total_price_all_cart': total_price_all_cart,
                            'total_count_all_cart': total_count_all_cart}

            return JsonResponse(data_message)


class MakeOrderView(View):
    model = Order

    def post(self, request, *args, **kwargs):
        data_message = {'message': '', 'error': False}

        order_services = OrderServices(user=request.user, model=self.model)
        cart_item_services = CartItemServices(user=request.user, model=CartItem)

        total_price = cart_item_services.get_total_price()

        user_balance = request.user.wallet.ballance
        is_user_money = user_balance < total_price

        form = OrderForm(request.POST)
        if not form.is_valid() and not is_user_money:
            data_message['error'] = True
            data_message['message'] = 'You don`t have enough money in your account'
            return JsonResponse(data_message)
        else:
            address = form.cleaned_data.get('address')

            product_all = cart_item_services.get_products_list()
            total_count = cart_item_services.get_total_count()

            order_services.order_create(total_price, total_count, product_all, address)
            cart_item_services.clear()
            return redirect('products:products_all')


class OrderView(ListView):
    model = Order
    template_name = 'orders/all_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        queryset = self.get_queryset()
        cart_item_all = queryset.filter(user=self.request.user)
        context['all_orders'] = cart_item_all
        return context


class ReservationView(ListView):
    model = Reservation
    template_name = 'orders/reserved_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        queryset = self.get_queryset()
        all_product_reservation = queryset.filter(user=self.request.user,
                                                  is_reserved=True)

        context['products_all'] = all_product_reservation
        return context


class DeleteReservationProduct(View):
    model = Reservation
    template_name = 'orders/reserved_products.html'

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        cart_item_services = ReservationServices(user=self.request.user,
                                                 model=self.model,
                                                 product_id=product_id)
        cart_item_services.deleting_reserved_product()
        return redirect('orders:reserved_products')
