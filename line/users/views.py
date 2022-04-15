from django.http import HttpResponseRedirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, tokens
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from users.forms import RegisterUserForm, GrantMoneyForm, ProfileEditForm, ImageForm
from users.models import User, Profile
from users.services import UserServices


class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "users/base.html", {})


class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = 'user_profile'


class ProfileUpdateView(View):

    def get(self, request, *args, **kwargs):

        data_image = {
            'image': request.user.profile.image.image,
        }

        data_profile = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'phone': request.user.profile.phone,
                'region': request.user.profile.region,
        }

        form_image = ImageForm(initial=data_image)
        form_profile = ProfileEditForm(initial=data_profile)

        data = {'form_image': form_image,
                'form_profile': form_profile,
                'id': request.user.profile.id
        }

        return render(
            request,
            'users/update_profile.html',
            data
        )

    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)
        form_profile = ProfileEditForm(request.POST)

        if form_profile.is_valid() or form.is_valid():

            image = request.FILES.get("image")

            first_name = form_profile.cleaned_data.get('first_name')
            last_name = form_profile.cleaned_data.get('last_name')
            phone = form_profile.cleaned_data.get('phone')
            region = form_profile.cleaned_data.get('region')

            user_services = UserServices(request.user, last_name, first_name, phone, region, image)
            user_services.update_profile()

        else:
            return redirect('home')

        return HttpResponseRedirect(reverse('users:profile', args=(request.user.profile.id,)))


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None
        if user and tokens.default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, _('The confirmation link was invalid,'
                                        ' possibly because it has already been used.'))
            return redirect('home')


class SignUpView(View):
    form_class = RegisterUserForm
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print('good')
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            form.send_email(request, user)

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class CustomActionView(PermissionRequiredMixin, View):
    permission_required = ['change_profile']

    @staticmethod
    def get(request, object_id):
        form = GrantMoneyForm()
        return render(
            request,
            'admin/users/grant_money.html',
            {'form': form}
        )

    @staticmethod
    def post(request, object_id):
        form = GrantMoneyForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data.get('amount')

            profile = Profile.objects.select_related('user__wallet').get(id=object_id)
            wallet_user = profile.user.wallet
            wallet_user.increase_balance(amount)
            return redirect('../')

