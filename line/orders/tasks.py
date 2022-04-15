import logging

from line.celery import app
from line.settings import AUTH_USER_MODEL
from app.email_notifications import send_purchase_of_goods_notification

User = AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@app.task(name="send_notification_new_order_product")
def send_purchase_of_goods_notification_task(*args):
    logger.info("Sent notification_reserved_product")
    return send_purchase_of_goods_notification(*args)
