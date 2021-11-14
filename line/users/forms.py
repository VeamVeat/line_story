from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from users.models import User


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label=_('first name'), widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label=_('last name'), widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label=_('repeat password'), widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
