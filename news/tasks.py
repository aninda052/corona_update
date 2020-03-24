
from . import data_collection
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime




def collect_news():
    print('News Collecting', datetime.now())
    data_collection.get_news_from_prothomAlo()
    data_collection.get_news_from_ittefak()
    data_collection.get_news_from_jugantor()
    data_collection.get_news_from_banglaNews24()
    # data_collection.get_news_from_dailyStar()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_news, 'interval', minutes=5)
    scheduler.start()