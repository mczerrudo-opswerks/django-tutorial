from django.contrib import admin
from django.contrib.auth import get_user_model
from core.models import Restaurant,Rating,Sales

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Rating)    
admin.site.register(Sales)
admin.site.register(get_user_model())