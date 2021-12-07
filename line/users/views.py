from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login, tokens
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from users.forms import RegisterUserForm, GrantMoneyForm, UserForm, ProfileForm
from users.models import User, Wallet, Profile


class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "users/base.html", {})


class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = 'user_profile'


# def products(request):
#     if request.method == "POST":
#         product_id = request.POST.get("product_pk")
#         product = Product.objects.get(id = product_id)
#         request.user.profile.products.add(product)
#         messages.success(request,(f'{product} added to wishlist.'))
#         return redirect ('main:products')
# 	products = Product.objects.all()
# 	paginator = Paginator(products, 18)
# 	page_number = request.GET.get('page')
# 	page_obj = paginator.get_page(page_number)
# 	return render(request = request, template_name="main/products.html", context = { "page_obj":page_obj})

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
