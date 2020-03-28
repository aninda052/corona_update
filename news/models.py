from django.db import models
from  django.utils.timezone import now







class news_paper(models.Model):
    news_paper_name = models.CharField(max_length=50)
    news_title = models.CharField(max_length=500)
    news_link = models.CharField(max_length=500)
    publication_time =models.CharField(max_length=30)

    data_fetching_time = models.DateTimeField(default=now)

    def __str__(self):
        return self.news_title

class world_casualties(models.Model):
    country_name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=8,default='NA')
    total_case = models.IntegerField()
    total_death = models.IntegerField()
    new_case = models.IntegerField()
    new_death = models.IntegerField()
    active_case = models.IntegerField()
    total_recovered = models.IntegerField()
    last_update =  models.DateTimeField(default=now)

    def __str__(self):
        return self.country_name





