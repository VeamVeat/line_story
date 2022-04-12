import logging

from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404
from django.contrib.auth import tokens

from users.models import User

logger = logging.getLogger(__name__)


def send_confirmation_mail(email):
    user = get_object_or_404(User, email=email)
    try:
        current_site = Site.objects.get_current().domain
        subject = 'Activate Your MySite Account'
        message = render_to_string('registration/account_active_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': tokens.default_token_generator.make_token(user),
        })
        user.email_user(subject, message)

    except Exception:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user.id)
