from io import StringIO
from PIL import Image
from django.core.files.storage import FileSystemStorage

from django.http import Http404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login, tokens
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import  DetailView

from line.settings import MEDIA_ROOT
from users.forms import RegisterUserForm, GrantMoneyForm, ProfileEditForm
from users.models import User, Profile
from users.services import UserServices, ProfileServices


class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "users/base.html", {})


class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = 'user_profile'


class ProfileUpdateView(View):

    def get(self, request, *args, **kwargs):
        form = ProfileEditForm()
        return render(
            request,
            'users/update_profile.html',
            {'form': form}
        )

    def post(self, request, *args, **kwargs):
        form = ProfileEditForm(request.POST, request.FILES)

        if form.is_valid():
            # image = form.cleaned_data['image']
            image = request.FILES['image']

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            region = form.cleaned_data.get('region')

            user_services = UserServices(request.user, User, last_name, first_name)
            user_services.update_full_name(first_name, last_name)

            profile_services = ProfileServices(request.user, Profile, phone, region)
            profile_services.update_profile(phone, region)

            if image:
                filename = FileSystemStorage().save(MEDIA_ROOT)

                user_services.update_image(filename)
                print(filename)

        else:
            return redirect('home')

        return redirect('home')


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
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

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': tokens.default_token_generator.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, _('Please Confirm your email to complete registration.'))

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
            wallet_user.save()
            return redirect('../')
