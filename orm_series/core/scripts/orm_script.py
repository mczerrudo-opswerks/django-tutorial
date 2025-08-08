from core.models import Restaurant, Rating, Sales
from django.utils import timezone
from django.db import connection
from django.contrib.auth import get_user_model
from pprint import pprint
def run():
    #User = get_user_model()
    # Create a new restaurant
    restaurants = Restaurant.objects.create(
        name='Aroma Cafe',
        website='https://aromacafe.com',
        date_opened=timezone.now() - timezone.timedelta(days=365),
        latitude=12.9715987,
        longitude=77.594566,
        address='123 Aroma Street, Bangalore',
        restaurant_type=Restaurant.TypeChoices.INDIAN
    )
    #print(Restaurant.objects.all())
   
    #pprint(connection.queries)  # Print all SQL queries executed during this run


