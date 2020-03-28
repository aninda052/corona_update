
from . import data_collection
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime



def get_casualties_data():
    print('World Casualties Data Collecting',datetime.now())
    data_collection.get_world_data()

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
    scheduler.add_job(get_casualties_data, 'interval', minutes=3)
    scheduler.start()