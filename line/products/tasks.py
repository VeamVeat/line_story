import logging

from line.celery import app
from app.email_notifications import send_notification_new_product, send_notification_reserved_product

logger = logging.getLogger(__name__)


@app.task(name="send_notification_new_product")
def send_notification_new_product_task(*args):
    logger.info("Sent notification new product")
    return send_notification_new_product(*args)


@app.task(name="send_notification_reserved_product")
def send_notification_reserved_product_task(*args):
    logger.info("Sent notification_reserved_product")
    return send_notification_reserved_product(*args)
