from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from users.models import User, Wallet, Profile


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label=_('first name'), widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label=_('last name'), widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label=_('repeat password'), widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class GrantMoneyForm(forms.Form):
    amount = forms.DecimalField()

    class Meta:
        model = Wallet
        fields = ('balance',)


class ProfileAdminForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput, max_length=255)

    def __init__(self, *args, **kwargs):
        super(ProfileAdminForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False

    class Meta:
        fields = '__all__'
        model = Profile
