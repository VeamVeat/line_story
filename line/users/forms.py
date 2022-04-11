from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model, password_validation
from django import forms

from line import settings
from products.models import File
from users.models import User, Wallet, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'birthday', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'region', )


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    birthday = forms.DateField(required=True,
                               widget=forms.DateInput(attrs={
                                   'placeholder': 'Birth Date',
                                   'class': 'form-control',
                                   'type': 'date',
                               }))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birthday', 'password1', 'password2')

    def clean_birthday(self):
        dob = self.cleaned_data['birthday']
        print(dob)
        today = now()
        age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day))
        print(age)
        if age < 18:
            raise forms.ValidationError('Must be at least 18 years old to register')
        return dob


class GrantMoneyForm(forms.Form):
    amount = forms.DecimalField()

    class Meta:
        model = Wallet
        fields = ('balance',)


class ProfileAdminForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput, max_length=255, required=False)

    class Meta:
        fields = '__all__'
        model = Profile


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(label=_('first name'), widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
    last_name = forms.CharField(label=_('last name'), widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
    phone = forms.CharField(max_length=17, required=False)
    region = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'region')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image', required=False)

    class Meta:
        model = File
        fields = ('image', )
