from datetime import datetime
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Event

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
    