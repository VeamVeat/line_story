from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render

from orders.models import CartItem, Order, Reservation
from orders.forms import OrderForm
from orders.services import OrderServices, CartItemServices, ReservationServices


class CartView(ListView):
    model = CartItem
    template_name = 'orders/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        queryset = self.get_queryset()
        cart_item_all = queryset.filter(user=self.request.user)

        cart_item_services = CartItemServices(user=self.request.user, model=self.model)

        total_price_and_total_count = cart_item_services.get_total_price_and_total_count()
        total_price_product = total_price_and_total_count['total_price']
        total_count_product = total_price_and_total_count['total_count']

        context['products_all'] = cart_item_all
        context['total_price_product'] = total_price_product
        context['total_count_product'] = total_count_product
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
    template_name = 'orders/cart.html'

    def post(self, request, *args, **kwargs):
        cart_item_all = self.model.objects.filter(user=self.request.user)
        product_id = kwargs.get('product_id')
        cart_item_services = CartItemServices(user=self.request.user,
                                              model=self.model,
                                              product_id=product_id)
        cart_item_services.diminish_product()

        return redirect('orders:cart')


class IncreaseProductView(ListView):
    model = CartItem
    template_name = 'orders/cart.html'

    def post(self, request, *args, **kwargs):
        cart_item_all = self.model.objects.filter(user=self.request.user)
        product_id = kwargs.get('product_id')
        cart_item_services = CartItemServices(user=self.request.user,
                                              model=self.model,
                                              product_id=product_id)
        cart_item_services.increase_product()

        return redirect('orders:cart')


class CheckoutView(View):
    model = CartItem
    template_name = 'orders/checkout.html'

    def post(self, request, *args, **kwargs):

        cart_item_services = CartItemServices(user=request.user, model=self.model)
        user_balance = request.user.wallet.ballance

        form = OrderForm()

        total_price_and_total_count = cart_item_services.get_total_price_and_total_count()
        total_price_product = total_price_and_total_count['total_price']
        total_count_product = total_price_and_total_count['total_count']

        if total_price_product > user_balance:
            return redirect('orders:not_money')

        product_cart_items = cart_item_services.get_all_cart_item()

        context = {'product_cart_items': product_cart_items, 'total_price': float(total_price_product),
                   'total_count': total_count_product, 'form': form}

        return render(request, self.template_name, context)


class MakeOrderView(View):
    model = Order

    def post(self, request, *args, **kwargs):
        order_services = OrderServices(user=request.user, model=self.model)
        cart_item_services = CartItemServices(user=request.user, model=CartItem)

        form = OrderForm(request.POST or None)

        if not form.is_valid():
            return redirect('orders:make_order')
        else:
            address = form.cleaned_data.get('address')

            product_all = cart_item_services.get_products_list()

            total_price_and_total_count = cart_item_services.get_total_price_and_total_count()
            total_price_product = total_price_and_total_count['total_price']
            total_count_product = total_price_and_total_count['total_count']

            order_services.order_create(total_price_product, total_count_product, product_all, address)

            cart_item_services.clear()

        return redirect('home')


class NotMoneyView(View):
    model = Order
    template_name = 'orders/not_money_notification.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={})


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
        all_product_reservation = queryset.filter(user=self.request.user, is_reserved=True)

        context['products_all'] = all_product_reservation
        return context


class DeleteReservationProduct(View):
    model = Reservation
    template_name = 'orders/cart.html'

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        cart_item_services = ReservationServices(user=self.request.user,
                                                 model=self.model,
                                                 product_id=product_id)
        cart_item_services.deleting_reserved_product()
        return redirect('orders:reserved_products')
