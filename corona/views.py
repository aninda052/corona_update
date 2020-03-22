from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import re


import plotly.graph_objects as go
from plotly.offline import plot
from pandas import DataFrame
import csv


def get_news_from_prothomAlo ():

    basePage = 'https://service.prothomalo.com/commentary/index.php'
    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")

    all_news = soup.find_all(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))
    all_news_link = [(news.get_text().strip(), news.get('href')) for news in all_news]

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    return all_news_link

def get_news_from_ittefak ():
    basePage = 'https://www.ittefaq.com.bd/all-news/covid19-update/?pg=1'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    _soup = soup.find_all('div', {'class': ['all_news_content_block']})

    all_news = _soup[0].find_all(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))
    all_news_link = [(news.get_text().strip(), news.get('href')) for news in all_news]

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    return all_news_link

def get_news_from_dailyStar():
    basePage = 'https://www.thedailystar.net/bangla/%E0%A6%B6%E0%A7%80%E0%A6%B0%E0%A7%8D%E0%A6%B7-%E0%A6%96%E0%A6%AC%E0%A6%B0'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    _soup = soup.find_all('div', {'class': ['two-50']})
    all_news = _soup[0].find_all(href=re.compile(r'[/]([a-z]|[A-Z])\w+'))
    all_news_link = [(news.get_text().strip(), news.get('href')) for news in all_news if len(news.get_text().strip()) >3]



    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    return all_news_link

def get_news_from_jugantor():
    basePage = 'https://www.jugantor.com/country-news/290844/%E0%A6%AE%E0%A6%BE%E0%A6%A6%E0%A6%BE%E0%A6%B0%E0%A7%80%E0%A6%AA%E0%A7%81%E0%A6%B0%E0%A7%87%E0%A6%B0-%E0%A6%B6%E0%A6%BF%E0%A6%AC%E0%A6%9A%E0%A6%B0-%E0%A6%B2%E0%A6%95%E0%A6%A1%E0%A6%BE%E0%A6%89%E0%A6%A8'

    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    all_news = soup.find_all('div', {'class': 'inner-box pull-left'})

    all_news_link = [(news.find('a').get_text().strip(), news.find('a').get('href')) for news in all_news]

    if len(all_news_link) > 5:
        all_news_link = all_news_link[:5]

    return all_news_link

def get_world_data():
    import os

    with open(os.getcwd() + '/corona/static/countries_codes.csv', newline='') as file:
        spamreader = csv.reader(file)
        country_to_iso_code = {country.lower(): code for country, code in spamreader}
    file.close()

    basePage = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(basePage)
    soup = BeautifulSoup(response.content, "html.parser")
    _soup = soup.find_all('table', {'id': ['main_table_countries_today']})[0].find_all('tr', {'style': ['']})

    data = []
    for row in _soup:
        _data = [re.sub('\W+', '', datapoint) for datapoint in row.get_text().split('\n')[1:-1]]
        #     print(_data)
        _data = [datapoint if datapoint else 0 for datapoint in _data]
        #     print
        country = _data[0].lower()
        if country not in country_to_iso_code:
            #         print(country)
            continue
        data.append([country, int(_data[1]), int(_data[3]), int(_data[2]), int(_data[5]), int(_data[8]) \
                        , int(_data[6]), country_to_iso_code[country]])

    return data


def get_heat_map():

    data = get_world_data()

    df = DataFrame(data, columns=['country', 'Total Affected', 'total_death', 'new_cases' \
        , 'new_death', 'active_cases', 'recovered', 'code'])



    # fig = px.choropleth(df, locations="code",
    #                     color="Total Affected",
    #                     hover_name="country",
    #                     range_color = [0, max(df['Total Affected'])+25000],
    #                     color_continuous_scale='mrybm')

    fig = go.Figure(data=go.Choropleth(
        locations=df["code"],
        z=df["Total Affected"],
        zmax = max(df['Total Affected'])+25000,
        text=df["country"],
        autocolorscale=True,
        reversescale=True,
    )
    )

    fig.update_layout(
        title_text="Aorona Affected Countries ",
        # xaxis=dict(
        #     tickmode='array',
        #     tickvals=[0,1],
        #     ticktext=['Female','Male']
        # ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style="carto-positron",

        width=1100,
        height=450,

    )


    return fig

def home_page(request):

    ''' Prothom Alo '''
    # prothom_alo_all_news_link = get_news_from_prothomAlo()
    # ittefak_all_news_link = get_news_from_ittefak()
    # jugantor_all_news_link = get_news_from_jugantor()
    # dailyStar_all_news_link = get_news_from_dailyStar()
    #
    # heat_map = get_heat_map()




    return render(request, 'index.html')

    # return render(request, 'home.html',{
    #     'prothom_alo_all_news_link' : prothom_alo_all_news_link,
    #     'ittefak_all_news_link' : ittefak_all_news_link,
    #     'jugantor_all_news_link' : jugantor_all_news_link,
    #     'dailyStar_all_news_link' : dailyStar_all_news_link,
    #     'heat_map': plot(heat_map, output_type='div',
    #                 include_plotlyjs=False, show_link=False, link_text=""),
    # })