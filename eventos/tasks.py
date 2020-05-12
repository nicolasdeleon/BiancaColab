# tring

# from django.contrib.auth.models import User
# from django.utils.crypto import get_random_string

# from celery import shared_task

# @shared_task
# def create_random_user_accounts(total):
#     for i in range(total):
#         username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
#         email = '{}@example.com'.format(username)
#         password = get_random_string(50)
#         User.objects.create_user(username=username, email=email, password=password)
#     return '{} random users created with success!'.format(total)

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import shared_task
from celery.utils.log import get_task_logger
from accounts.models import User
from datetime import datetime
from .models import Event

logger = get_task_logger(__name__)

# @shared_task
# def test_celery_worker():
#     print("Celery Workers are working fine.")
 
# A periodic task that will run every minute (the symbol "*" means every)
#@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
@shared_task
def close_events():
    logger.info("Task close event started")
    if Event.objects.filter(status="O").filter(endDate__lte=datetime.now()).count()>0:
    	queryset = Event.objects.filter(status="O").filter(endDate__lte=datetime.now())
    	for each in queryset:
            each.status="F"
            each.save()
    else:
    	return "NO events to close"

    return "Task close event finished"