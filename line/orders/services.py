from django.db import models
from django.db.models import F, QuerySet
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from products.models import Product


class OrderServices:
    def __init__(self,
                 user,
                 model=None,
                 product_id=None,
                 object_id=None):

        self.user = user
        self.object_id = object_id
        self.model = model
        self.product_id = product_id

    def order_create(self, total_price_product, total_count_product, product_all, address):
        self.model.objects.create(
            user=self.user,
            quantity=total_count_product,
            final_price=total_price_product,
            product_list={'products': product_all},
            address=address
        )
        order_user = get_object_or_404(self.model, user=self.user, is_active=True)

        subject = 'your order has been completed'
        message = render_to_string('orders/new_order_notification.html', {
            'user': self.user,
            'count': order_user.quantity,
            'price': order_user.final_price
        })

        self.user.email_user(subject, message)

        order_user.is_active = False
        order_user.save()


class CartItemServices:
    def __init__(self,
                 user,
                 model=None,
                 product_id=None,
                 object_id=None):

        self.user = user
        self.object_id = object_id
        self.model = model
        self.product_id = product_id

    def get_all_cart_item(self) -> QuerySet:
        return self.model.objects.filter(user=self.user).select_related('product')

    def __get_product_in_cart_by_product_id(self):
        cart_product = get_object_or_404(self.model.objects.select_related('product'),
                                      user=self.user,
                                      product_id=self.product_id)
        return cart_product

    def get_total_price(self) -> int:
        cart_item_current_user = self.get_all_cart_item()
        total_price = cart_item_current_user.aggregate(total_price=models.Sum(F('product__price') * F('quantity')))
        return total_price['total_price']

    def get_total_count(self) -> int:
        cart_item_current_user = self.get_all_cart_item()
        total_count = cart_item_current_user.aggregate(total_count=models.Sum(F('quantity')))
        return total_count['total_count']

    def get_quantity_product_in_cart(self):
        product = self.__get_product_in_cart_by_product_id()
        return product.quantity

    def calculate_product(self, param='increase'):
        product_success = True

        product_in_cart = self.__get_product_in_cart_by_product_id()
        product = get_object_or_404(Product, id=self.product_id)

        if param == 'increase':
            if not product.is_stock:
                product_success = False
                return product_success

            product.quantity -= 1
            product.save()

            product_in_cart.quantity += 1
            product_in_cart.save()

            return product_success
        elif param == 'diminish':
            if product_in_cart.quantity == 1:
                product_success = False
                return product_success

            product.quantity += 1
            product.save()

            product_in_cart.quantity -= 1
            product_in_cart.save()

            return product_success

    def get_products_list(self):
        cart_item_current_user = self.get_all_cart_item()
        all_products_in_the_dict = [product.product.get_product_in_the_dict for product in cart_item_current_user]
        return all_products_in_the_dict

    def delete_product(self):
        product_in_cart = get_object_or_404(self.model, user=self.user, product_id=self.product_id)
        product = get_object_or_404(Product, id=self.product_id)

        product.quantity += product_in_cart.quantity
        product.save()

        product_in_cart.delete()

    def add_product(self):
        product = get_object_or_404(Product, id=self.product_id)

        self.model.objects.create(user=self.user, product_id=product.id)
        product.quantity -= 1
        product.save()

    def clear(self):
        self.model.objects.filter(user=self.user).delete()


class ReservationServices:
    def __init__(self,
                 user,
                 model=None,
                 product_id=None,
                 count_product=None):

        self.user = user
        self.model = model
        self.product_id = product_id
        self.count_product = count_product

    def make_reservation(self):
        product = get_object_or_404(Product, id=self.product_id)
        if product.quantity >= self.count_product:
            object_reservation = self.model(user=self.user,
                                            quantity=self.count_product,
                                            product_id=product.id)

            product.quantity -= self.count_product
            product.save()

            object_reservation.is_reserved = True
            object_reservation.save()

            subject = 'your item is reserved'
            message = render_to_string('orders/new_reserved_notification.html', {
                'user': self.user,
                'count': object_reservation.quantity,
                'price': object_reservation.product.price,
                'time': object_reservation.created_at
            })

            self.user.email_user(subject, message)
            return True
        else:
            return False

    def deleting_reserved_product(self):
        reserved_product = get_object_or_404(self.model, user=self.user, product_id=self.product_id)
        product = get_object_or_404(Product, id=self.product_id)

        product.quantity += reserved_product.quantity
        product.save()

        reserved_product.delete()
