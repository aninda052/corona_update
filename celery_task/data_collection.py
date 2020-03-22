from bs4 import BeautifulSoup
import requests
import re
from corona.models import news_paper
from datetime import datetime

def insert_data(paper_name, data):

    for news_title, news_link, pulication_time in data:

        paper = news_paper()
        paper.news_paper_name = paper_name
        paper.news_title = news_title
        paper.news_link = news_link
        paper.publication_time = pulication_time
        paper.data_fetching_time = datetime.now()

        paper.save()

def get_news_from_prothomAlo ():

    basePage = 'https://service.prothomalo.com/commentary/index.php'
    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    soup = soup.find_all('div', {'class': 'score-content'})

    all_news_link = []
    for news in soup:
        tmp = news.find(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))
        if tmp:
            date = news.find('div', {'class': 'time'}).get_text().split('\n')[2:]
            date = ','.join([i.strip() for i in date[::-1]])
            title = tmp.get_text().strip()
            link = tmp.get('href')
            all_news_link.append([title, link, date])


    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data('prothom alo', all_news_link)


    # return all_news_link

def get_news_from_ittefak ():
    basePage = 'https://www.ittefaq.com.bd/all-news/covid19-update/?pg=1'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    _soup = soup.find_all('div', {'class': ['all_news_content_block']})

    all_news = _soup[0].find_all(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))
    all_news_link = [(news.get_text().strip(), news.get('href')) for news in all_news]

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data('ittefak', all_news_link)

    # return all_news_link

def get_news_from_dailyStar():
    basePage = 'https://www.thedailystar.net/bangla/%E0%A6%B6%E0%A7%80%E0%A6%B0%E0%A7%8D%E0%A6%B7-%E0%A6%96%E0%A6%AC%E0%A6%B0'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    _soup = soup.find_all('div', {'class': ['two-50']})
    all_news = _soup[0].find_all(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))
    all_news_link = [(news.get_text().strip(), news.get('href')) for news in all_news if len(news.get_text().strip()) >3]



    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data('daily star', all_news_link)

    # return all_news_link

def get_news_from_jugantor():
    basePage = 'https://www.jugantor.com/country-news/290844/%E0%A6%AE%E0%A6%BE%E0%A6%A6%E0%A6%BE%E0%A6%B0%E0%A7%80%E0%A6%AA%E0%A7%81%E0%A6%B0%E0%A7%87%E0%A6%B0-%E0%A6%B6%E0%A6%BF%E0%A6%AC%E0%A6%9A%E0%A6%B0-%E0%A6%B2%E0%A6%95%E0%A6%A1%E0%A6%BE%E0%A6%89%E0%A6%A8'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    all_news = soup.find_all('div', {'class': 'inner-box pull-left'})

    all_news_link = [(news.find('a').get_text().strip(), news.find('a').get('href')) for news in all_news]

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data('jugantor', all_news_link)

    # return all_news_link