from core.models import Restaurant, Rating, Sales
from django.utils import timezone
from django.db import connection
from django.contrib.auth import get_user_model
from pprint import pprint
def run():
    User = get_user_model()
    # Create a new restaurant
    restaurant = Restaurant.objects.first()
    user = User.objects.first()
    print(restaurant.name)
    
    restaurant.name = 'A New Restaurant Name'
    restaurant.save(update_fields=['name'])  # Save the changes to the database
   
    pprint(connection.queries)  # Print all SQL queries executed during this run


