from django.contrib import admin
from .models import City, Restaurant, Donation, NewsItem

# Register your models here.

admin.site.register(City)
admin.site.register(Restaurant)
admin.site.register(NewsItem)
admin.site.register(Donation)