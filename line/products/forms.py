from django import forms
from django.utils.translation import gettext_lazy as _
from products.models import Product
from orders.models import Reservation


class ProductAdminForm(forms.ModelForm):

    image = forms.ImageField(widget=forms.FileInput, max_length=255)

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    class Meta:
        fields = '__all__'
        model = Product


class NumberOfProductForm(forms.ModelForm):

    quantity = forms.NumberInput()

    class Meta:
        model = Reservation
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'id': 'post-number',
                'required': True,
            }),
        }


