import json
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView

from orders.models import CartItem, Reservation
from orders.services import CartItemServices, ReservationServices
from products.forms import NumberOfProductForm
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
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        contex = super(ProductView, self).get_context_data(**kwargs)
        product_services = ProductServices(user=self.request.user,
                                           model=self.model)

        contex['all_product_in_cart'] = product_services.get_all_product_id_in_cart()
        contex['form'] = NumberOfProductForm()
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


class AddProduct(View):

    def post(self, request, *args, **kwargs):
        data_message = {'message': ''}
        if is_ajax(request=request):
            data = json.load(request)
            product_id = data.get('product_id')
            product_services = ProductServices(user=self.request.user,
                                               model=Product,
                                               product_id=product_id)

            cart_item_services = CartItemServices(user=self.request.user,
                                                  model=CartItem,
                                                  product_id=product_id)

            cart_item_services.add_product()
            product = product_services.get_product()

            data_message['message'] = f'the product {product.title} was successfully added to the cart'

        return JsonResponse(data_message)


class FilterProductView(TypeYearsProduct, ListView):
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


class SearchResultsView(TypeYearsProduct, ListView):
    model = Product
    template_name = 'products/products_all.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        text_search = self.request.GET.get('search')

        if text_search:
            queryset = queryset.filter(Q(title__icontains=text_search) |
                                       Q(type__name__icontains=text_search))
        return queryset


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class MakeReservation(View):

    def post(self, request, *args, **kwargs):
        data_message = {'message': '', 'error': False}

        if is_ajax(request=request):
            data = json.load(request)
            product_id = data.get('product_id')
            number_product = data.get('number_product')

            number_product = int(number_product)
            reservation_services = ReservationServices(user=request.user,
                                                       model=Reservation,
                                                       count_product=number_product,
                                                       product_id=product_id)

            reservation_success = reservation_services.make_reservation()
            if not reservation_success:
                data_message['error'] = True
                data_message['message'] = 'the selected quantity exceeds the quantity in stock'

        return JsonResponse(data_message)
