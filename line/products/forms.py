from django import forms
from django.utils.translation import ugettext_lazy as _

from products.models import Product


class ProductAdminForm(forms.ModelForm):

    image = forms.ImageField(widget=forms.FileInput, max_length=255)
    product_type = forms.CharField(max_length=255,
                                   widget=forms.TextInput(attrs={'placeholder': _('enter new product type')}))

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['product_type'].required = False

    class Meta:
        fields = '__all__'
        model = Product
