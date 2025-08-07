from core.models import Restaurant, Rating, Sales
from django.utils import timezone
from django.db import connection
from django.contrib.auth import get_user_model
from pprint import pprint
def run():
    User = get_user_model()
    # Create a new restaurant
    restaurants = Restaurant.objects.filter(name__startswith='A')
    print(restaurants)
    print(restaurants.update(
        date_opened = timezone.now() -timezone.timedelta(days=365),
    ))
    pprint(connection.queries)  # Print all SQL queries executed during this run


