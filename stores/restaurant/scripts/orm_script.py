from restaurant.models import Restaurant, Rating, Sales
from django.utils import timezone
from django.db import connection
from django.contrib.auth import get_user_model
from pprint import pprint
import random
def run():
    #User = get_user_model()
    # Create a 20 Test Restaurant
    """ for i in range(1, 21):
        Restaurant.objects.create(
            name=f"Test Restaurant {i}",
            website=f"https://test{i}.com",
            date_opened=timezone.now() - timezone.timedelta(days= i * 30),
            latitude=12.9715987 + random.uniform(-0.01, 0.01),
            longitude=77.594566 + random.uniform(-0.01, 0.01),
            address=f"{123 + i} Test Street, Bangalore",
            restaurant_type=Restaurant.TypeChoices.INDIAN
        ) """
    
    #print(Restaurant.objects.all())
   
    pprint(connection.queries)  # Print all SQL queries executed during this run


