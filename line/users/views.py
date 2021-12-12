from io import StringIO
from PIL import Image

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
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, UpdateView

from products.models import File
from users.forms import RegisterUserForm, GrantMoneyForm, UserForm, ProfileForm, ProfileEditForm
from users.models import User, Wallet, Profile


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
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            region = form.cleaned_data.get('region')

            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.save(update_fields=['first_name', 'last_name', 'birthday'])

            user_profile = Profile.objects.get(user=request.user)
            user_profile.phone = phone
            user_profile.region = region
            user_profile.save(update_fields=['phone', 'region'])

            # if user_profile.image:
            #     profile_file = File.objects.get(id=user_profile.image.id)
            #     profile_file.image = image
            #     profile_file.save(update_fields=['image'])
            # else:
            #     profile_file = File.objects.create(image=g_image)
            #     user_profile.image = profile_file
            #     profile_file.save(update_fields=['image'])

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
            wallet = Wallet.objects.get(user=object_id)
            wallet.increase_balance(amount)
            wallet.save()
            return redirect('../')


# class ProfileUpdateView(UpdateView):
#     model = Profile
#     form_class = ProfileForm
#     template_name = 'users/update_profile.html'
#     success_url = '/'

    # def get_object(self, **kwargs):
    #     username = self.kwargs.get("username")
    #     if username is None:
    #         raise Http404
    #     return get_object_or_404(Profile, user__username__iexact=username)
