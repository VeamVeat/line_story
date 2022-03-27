from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):

    address = forms.CharField(max_length=255)

    class Meta:
        model = Order
        fields = (
            'address',
        )
