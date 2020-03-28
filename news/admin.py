from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import news_paper, world_casualties

admin.site.register(news_paper)
admin.site.register(world_casualties)