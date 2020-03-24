from bs4 import BeautifulSoup
import requests
import re
from .models import news_paper
from datetime import datetime

def insert_data(paper_name, data):

    for news_title, news_link, pulication_time in data:

        paper, created = news_paper.objects.get_or_create(news_paper_name = paper_name,news_title = news_title )

        if created:
            paper.news_link = news_link
            paper.publication_time = pulication_time

            paper.save()

def get_news_from_prothomAlo ():
    basePage = 'https://www.prothomalo.com/topic/%E0%A6%95%E0%A6%B0%E0%A7%8B%E0%A6%A8%E0%A6%BE%E0%A6%AD%E0%A6%BE%E0%A6%87%E0%A6%B0%E0%A6%BE%E0%A6%B8'
    # basePage = 'https://service.prothomalo.com/commentary/index.php'
    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    all_news_link = []

    soup = soup.find_all('div', {'class': 'col col1'})
    for news in soup:
        title = news.find('span', {'class': 'title'}).get_text()
        link = "https://www.prothomalo.com/" + news.find('a').get('href')
        all_news_link.append([title, link, ''])


    # soup = soup.find_all('div', {'class': 'score-content'})
    # for news in soup:
    #     tmp = news.find(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))
    #     if tmp:
    #         date = news.find('div', {'class': 'time'}).get_text().split('\n')[2:]
    #         date = ','.join([i.strip() for i in date[::-1]])
    #         title = tmp.get_text().strip()
    #         link = tmp.get('href')
    #         all_news_link.append([title, link, date])


    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data('prothomAlo', all_news_link)




def get_news_from_ittefak ():
    basePage = 'https://www.ittefaq.com.bd/all-news/covid19-update/?pg=1'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    _soup = soup.find_all('div', {'class': ['all_news_content_block']})

    all_news = _soup[0].find_all(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))

    all_news_link = []
    for news in all_news:
        title = date = news.find('div', {'class': 'hl'}).get_text()
        link = news.get('href')
        date = news.find('div', {'class': 'post_date'}).get_text()
        all_news_link.append([title, link, date])

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data('ittefak', all_news_link)


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



def get_news_from_jugantor():
    basePage = 'https://www.jugantor.com/country-news/290844/%E0%A6%AE%E0%A6%BE%E0%A6%A6%E0%A6%BE%E0%A6%B0%E0%A7%80%E0%A6%AA%E0%A7%81%E0%A6%B0%E0%A7%87%E0%A6%B0-%E0%A6%B6%E0%A6%BF%E0%A6%AC%E0%A6%9A%E0%A6%B0-%E0%A6%B2%E0%A6%95%E0%A6%A1%E0%A6%BE%E0%A6%89%E0%A6%A8'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    all_news = soup.find_all('div', {'class': 'inner-box pull-left'})

    all_news_link = [(news.find('a').get_text().strip(), news.find('a').get('href'),'') for news in all_news]

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data('jugantor', all_news_link)

def get_news_from_banglaNews24():

    basePage = 'https://www.banglanews24.com/topic/%E0%A6%95%E0%A6%B0%E0%A7%8B%E0%A6%A8%E0%A6%BE-%E0%A6%AD%E0%A6%BE%E0%A6%87%E0%A6%B0%E0%A6%BE%E0%A6%B8'
    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")

    soup = soup.find_all('div', {'class': 'col-sm-8'})
    all_news_link = [(news.find('a').get_text().strip(), news.find('a').get('href'), '') for news in soup]

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data('banglaNews24', all_news_link)

