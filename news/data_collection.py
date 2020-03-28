from bs4 import BeautifulSoup
import requests
import re
from .models import news_paper,world_casualties

from  django.utils.timezone import now


def insert_data_into_news_paper_table(paper_name, data):

    for news_title, news_link, pulication_time in data:

        obj, created = news_paper.objects.get_or_create(news_paper_name = paper_name,news_title = news_title
                                                          ,defaults = {
                                                                    'news_link' : news_link,
                                                                    'publication_time' : pulication_time

                                                        } )

def insert_data_into_world_casualties_table(country, data, country_code= "NA" ):

    total_case, total_death, new_case, new_death = int(data[1]), int(data[3]), int(data[2]), int(data[4])
    active_case, total_recovered = int(data[6]), int(data[5])


    obj, created = world_casualties.objects.update_or_create(country_name=country,defaults = {
                                                                                        'total_case' : total_case,
                                                                                        'total_death' : total_death,
                                                                                        'new_case' : new_case,
                                                                                        'new_death' : new_death,
                                                                                        'active_case' : active_case,
                                                                                        'total_recovered' : total_recovered,
                                                                                        'country_code' : country_code,
                                                                                        'last_update' : now
                                                                                        })



def get_world_data():
    import os
    from csv import reader

    with open(os.getcwd() + '/news/static/countries_codes.csv', newline='') as file:
        spamreader = reader(file)
        country_to_iso_code = {country.lower(): code for country, code in spamreader}
    file.close()

    basePage = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    _soup = soup.find_all('table', {'id': ['main_table_countries_today']})[0].find_all('tr', {'style': ['']})


    for row in _soup:
        data = [re.sub('\W+', '', datapoint) for datapoint in row.get_text().split('\n')[1:-1]]

        data = [datapoint if datapoint else 0 for datapoint in data]
        country = data[0].lower()

        if country not in country_to_iso_code:
            # print(country)
            country_code = "NA"
        else:
            country_code = country_to_iso_code[country]

        insert_data_into_world_casualties_table(country, data, country_code)

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


    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data_into_news_paper_table('prothomAlo', all_news_link)

def get_news_from_ittefak ():
    basePage = 'https://www.ittefaq.com.bd/all-news/covid19-update/?pg=1'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    _soup = soup.find_all('div', {'class': ['all_news_content_block']})

    all_news = _soup[0].find_all(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))

    all_news_link = []
    for news in all_news:
        title = news.find('div', {'class': 'hl'}).get_text()
        link = news.get('href')
        date = news.find('div', {'class': 'post_date'}).get_text()
        all_news_link.append([title, link, date])

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data_into_news_paper_table('ittefak', all_news_link)

def get_news_from_dailyStar():
    basePage = 'https://www.thedailystar.net/bangla/%E0%A6%B6%E0%A7%80%E0%A6%B0%E0%A7%8D%E0%A6%B7-%E0%A6%96%E0%A6%AC%E0%A6%B0'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    _soup = soup.find_all('div', {'class': ['two-50']})
    all_news = _soup[0].find_all(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))
    all_news_link = [(news.get_text().strip(), news.get('href')) for news in all_news if len(news.get_text().strip()) >3]



    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data_into_news_paper_table('daily star', all_news_link)

def get_news_from_jugantor():
    basePage = 'https://www.jugantor.com/country-news/290844/%E0%A6%AE%E0%A6%BE%E0%A6%A6%E0%A6%BE%E0%A6%B0%E0%A7%80%E0%A6%AA%E0%A7%81%E0%A6%B0%E0%A7%87%E0%A6%B0-%E0%A6%B6%E0%A6%BF%E0%A6%AC%E0%A6%9A%E0%A6%B0-%E0%A6%B2%E0%A6%95%E0%A6%A1%E0%A6%BE%E0%A6%89%E0%A6%A8'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    all_news = soup.find_all('div', {'class': 'inner-box pull-left'})

    all_news_link = [(news.find('a').get_text().strip(), news.find('a').get('href'),'') for news in all_news]

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data_into_news_paper_table('jugantor', all_news_link)

def get_news_from_banglaNews24():

    basePage = 'https://www.banglanews24.com/topic/%E0%A6%95%E0%A6%B0%E0%A7%8B%E0%A6%A8%E0%A6%BE-%E0%A6%AD%E0%A6%BE%E0%A6%87%E0%A6%B0%E0%A6%BE%E0%A6%B8'
    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")

    soup = soup.find_all('div', {'class': 'col-sm-8'})
    all_news_link = [(news.find('a').get_text().strip(), news.find('a').get('href'), '') for news in soup]

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    insert_data_into_news_paper_table('banglaNews24', all_news_link)

