from django.db import models
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from products.models import ProductFile, Product


class OrderServices:
    def __init__(self, user, model=None, product_id=None, odject_id=None):
        self.user = user
        self.object_id = odject_id
        self.model = model
        self.product_id = product_id

    def order_create(self, total_price_product, total_count_product, product_all):
        self.model.objects.create(
            user=self.user,
            quantity=total_count_product,
            final_price=total_price_product,
            product_list={'products': product_all}
        )

    def checkout(self, address):

        order_user = self.model.objects.get(user=self.user, is_active=True)
        money = self.user.wallet
        is_checkout = True

        if order_user.final_price > money.ballance:
            self.model.objects.filter(user=self.user, is_active=True).delete()
            is_checkout = False
        else:
            self.user.diminish_balance(order_user.final_price)
            order_user.address = address
            order_user.is_active = False
            order_user.save(update_fields=['address', 'is_active'])

            subject = 'your order has been completed'
            message = render_to_string('orders/new_order_notification.html', {
                'user': self.user,
                'count': order_user.quantity,
                'price': order_user.final_price
            })
            self.user.email_user(subject, message)
        return is_checkout


class CartItemServices:
    def __init__(self, user, model=None, product_id=None, odject_id=None):
        self.user = user
        self.object_id = odject_id
        self.model = model
        self.product_id = product_id

    def _get_all_cart_item(self):
        return self.model.objects.filter(user=self.user)

    def get_total_price_and_total_count(self):
        cart_item_current_user = self._get_all_cart_item()
        total_price_and_total_count = cart_item_current_user.aggregate(total_price=models.Sum(F('product__price')
                                                                                              * F('quantity')),
                                                                       total_count=models.Count('product__quantity'))
        return total_price_and_total_count

    def get_products(self):
        cart_item_current_user = self._get_all_cart_item()
        all_products_in_the_dict = [product.product.get_product_in_the_dict for product in cart_item_current_user]
        return all_products_in_the_dict

    def delete_product(self):
        product = get_object_or_404(self.model, user=self.user, product_id=self.product_id)
        product.delete()

    def add_product(self):
        product = get_object_or_404(Product, id=self.product_id)

        object_cart, create_cart = self.model.objects.get_or_create(user=self.user, product_id=product.id)
        if not create_cart:
            object_cart.quantity += 1
            object_cart.save()

    def clear(self):
        self.model.objects.filter(user=self.user).delete()
