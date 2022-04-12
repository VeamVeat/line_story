import logging

from line.celery import app
from line.settings import AUTH_USER_MODEL
from users.email import send_confirmation_mail

User = AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@app.task(name="send_confirmation_mail_task")
def send_confirmation_mail_task(email):
    logger.info("Sent Confirmation Email")
    return send_confirmation_mail(email)
