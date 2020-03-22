from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
# from celery.utils.log import get_task_logger
#
#
# logger = get_task_logger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corona.settings')
app = Celery('corona')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


from celery.task import periodic_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)





@periodic_task(name="debug_task ",run_every=crontab(minute='*/2'))
def debug_task():
    logger.info('Celery Working')




