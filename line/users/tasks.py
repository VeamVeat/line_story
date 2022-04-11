import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, tokens
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_bytes

from line.celery import app

logger = logging.getLogger(__name__)


@app.task
def send_verification_email(request_user):
    try:
        current_site = get_current_site(request_user)
        subject = 'Activate Your MySite Account'
        message = render_to_string('registration/account_active_email.html', {
            'user': request_user.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(request_user.user.pk)),
            'token': tokens.default_token_generator.make_token(request_user.user),
        })
        request_user.user.email_user(subject, message)

        messages.success(request_user, _('Please Confirm your email to complete registration.'))
    except Exception:
        logging.warning("Tried to send verification email to non-existing user '%s'" % request_user.user.id)


@app.task
def supper_sum(x, y):
    print(x + y)
