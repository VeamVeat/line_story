from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

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
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label=_('first name'), widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label=_('last name'), widget=forms.TextInput(attrs={'class': 'form-input'}))
    birthday = forms.DateField(label=_('date of birthday'), widget=forms.SelectDateWidget(years=range(1900, now().year)))
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label=_('repeat password'), widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birthday', 'password1', 'password2')

    def clean_birthday(self):
        dob = self.cleaned_data['birthday']
        today = now()
        age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day))
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
    # доработать загрузку фото
    image = forms.ImageField()
    first_name = forms.CharField(label=_('first name'), widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label=_('last name'), widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Profile
        fields = ('image', 'first_name', 'last_name', 'phone', 'region')

