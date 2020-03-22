from celery.task import periodic_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from . import data_collection

logger = get_task_logger(__name__)





@periodic_task(name="collect_news ",run_every=crontab(minute='*/2'))
def collect_news():
    logger.info('News Collecting')
    data_collection.get_news_from_prothomAlo()
    # data_collection.get_news_from_ittefak()
    # data_collection.get_news_from_jugantor()
    # data_collection.get_news_from_dailyStar()

# @periodic_task(name="collect_news ",run_every=crontab(minute='*/2'))
# def collect_news():
#     logger.info('Celery Working')