from django.shortcuts import render

import plotly.graph_objects as go
from plotly.offline import plot
from pandas import DataFrame
from .models import news_paper,world_casualties
from bangla import convert_english_digit_to_bangla_digit as to_bangla






def get_heat_map():

    data = world_casualties.objects.all().values()
    data = [[i['country_name'], i['total_case'], i['total_death'], i['new_case'], i['new_death'], i['active_case'],i['total_recovered'], i['country_code']] for i in data]

    df = DataFrame(data, columns=['country', 'Total Affected', 'total_death', 'new_cases', 'new_death', 'active_cases', 'recovered', 'code'])

    _sum = df.sum()
    _sum_bd = df[df['country']=='bangladesh'].sum()

    data = {}
    data['total_case'], data['total_death'], data['active_cases'], data['recovered'] = to_bangla(_sum['Total Affected']),  to_bangla(_sum['total_death'])\
                                                                                    ,  to_bangla(_sum['active_cases']),  to_bangla(_sum['recovered'])
    data['bd_total_case'], data['bd_total_death'], data['bd_active_cases'], data['bd_recovered'] = to_bangla(_sum_bd['Total Affected']),  to_bangla(_sum_bd['total_death'])\
                                                                                                ,  to_bangla(_sum_bd['active_cases']),  to_bangla(_sum_bd['recovered'])

    df = df[df['code'] != 'NA']

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
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style="carto-positron",
        width=800,
        height=400,

    )


    return fig, data

def home_page(request):



    prothom_alo_all_news_link = news_paper.objects.filter(news_paper_name = 'prothomAlo').values( 'news_title', 'news_link', 'publication_time').order_by('-data_fetching_time')[:15]
    ittefak_all_news_link = news_paper.objects.filter(news_paper_name = 'ittefak').values( 'news_title', 'news_link', 'publication_time').order_by('-data_fetching_time')[:15]
    jugantor_all_news_link = news_paper.objects.filter(news_paper_name = 'jugantor').values( 'news_title', 'news_link', 'publication_time').order_by('-data_fetching_time')[:15]
    banglaNews24_all_news_link = news_paper.objects.filter(news_paper_name = 'banglaNews24').values( 'news_title', 'news_link', 'publication_time').order_by('-data_fetching_time')[:15]
    # dailyStar_all_news_link = news_paper.object.filter(news_paper_name = 'daily star')[:5]
    #
    heat_map, data = get_heat_map()




    return render(request, 'home.html',{
        # 'total_case':total_case,
        # 'total_death':total_death,
        # 'active_cases':active_cases,
        # 'recovered':recovered,
        'data':data,
        'prothom_alo_all_news_link' : prothom_alo_all_news_link,
        'ittefak_all_news_link' : ittefak_all_news_link,
        'jugantor_all_news_link' : jugantor_all_news_link,
        'banglaNews24_all_news_link' : banglaNews24_all_news_link,
        # 'dailyStar_all_news_link' : dailyStar_all_news_link,
        'heat_map': plot(heat_map, output_type='div',
                    include_plotlyjs=False, show_link=False, link_text=""),
    })

