from datetime import datetime
from celery import shared_task
from celery.utils.log import get_task_logger
from exponent_server_sdk import (PushClient, PushMessage,
                                 PushServerError)
from accounts.models import User
from .models import Event, Post

logger = get_task_logger(__name__)


@shared_task
def close_events():
    logger.info("Task close event started")
    if Event.objects.filter(status="O").filter(endDate__lte=datetime.now()).count() > 0:
        queryset = Event.objects.filter(status="O").filter(endDate__lte=datetime.now())
        for each in queryset:
            each.status = "F"
            each.save()
    else:
        return "NO events to close"
    return "Events closed"


@shared_task
def send_message():
    logger.info("Task close event started")
    user = User.objects.filter(email="damianedona@gmail.com")
    post = Post.objects.filter(person=user)

    try:
        response = PushClient().publish(
            PushMessage(to=post.notificationToken,
                        body="send_message"))
        return response
    except PushServerError as exc:
        raise exc
