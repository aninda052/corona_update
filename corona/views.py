from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import re


import plotly.graph_objects as go
from plotly.offline import plot
from pandas import DataFrame
import csv
from .models import news_paper




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

    prothom_alo_all_news_link = news_paper.objects.filter(news_paper_name = 'prothom alo').values( 'news_title', 'news_link', 'publication_time')[:5]
    # print(prothom_alo_all_news_link)
    # ittefak_all_news_link = news_paper.object.filter(news_paper_name = 'ittefak')[:5]
    # jugantor_all_news_link = news_paper.object.filter(news_paper_name = 'jugantor')[:5]
    # dailyStar_all_news_link = news_paper.object.filter(news_paper_name = 'daily star')[:5]
    #
    # heat_map = get_heat_map()




    return render(request, 'index.html',{
        'prothom_alo_all_news_link' : prothom_alo_all_news_link
    })

    # return render(request, 'home.html',{
    #     'prothom_alo_all_news_link' : prothom_alo_all_news_link,
    #     'ittefak_all_news_link' : ittefak_all_news_link,
    #     'jugantor_all_news_link' : jugantor_all_news_link,
    #     'dailyStar_all_news_link' : dailyStar_all_news_link,
    #     'heat_map': plot(heat_map, output_type='div',
    #                 include_plotlyjs=False, show_link=False, link_text=""),
    # })