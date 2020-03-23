from django.db import models
from datetime import datetime




## PostGresSQL DataBase Starts ##

class news_paper(models.Model):
    news_paper_name = models.CharField(max_length=50)
    news_title = models.CharField(max_length=500)
    news_link = models.CharField(max_length=500)
    publication_time =models.CharField(max_length=30)

    data_fetching_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.news_title



