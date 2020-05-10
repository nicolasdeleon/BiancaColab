from celery import Celery

from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab

logger = get_task_logger(__name__)


# @periodic_task(
#     run_every=(crontab(minute='*/15')),
#     name="task_save_latest_flickr_image",
#     ignore_result=True
# )
# def task_save_latest_flickr_image():
#     """
#     Saves latest image from Flickr
#     """
#     logger.info("Saved image from Flickr")

from celery import task 
from celery import shared_task 
# We can have either registered task 
@task(name='summary') 
def send_import_summary():
     # Magic happens here ... 
# or 
@shared_task 
def send_notifiction():
     print('Here Im')
     logger.info("Saved image from Flickr")