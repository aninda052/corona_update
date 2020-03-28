


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import news_paper




class get_news(APIView):

    def get(self, request, *args, **kwargs):

        paperName = self.kwargs['paperName']

        # cashTime = 57600 # caching time at client-end in second
        # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Cache-Control': 'max-age={}'.format(cashTime)}

        ittefak_all_news_link = news_paper.objects.filter(news_paper_name=paperName).values('news_title', 'news_link',
                                                                                            'publication_time').order_by('-data_fetching_time')[:15]

        return Response(ittefak_all_news_link)