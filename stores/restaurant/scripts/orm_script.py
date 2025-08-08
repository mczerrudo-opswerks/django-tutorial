from restaurant.models import Restaurant, Rating, Sales
from django.utils import timezone
from django.db import connection
from django.contrib.auth import get_user_model
from pprint import pprint
import random
def run():
   
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

    # Create 20 User
    """ User = get_user_model()
    for i in range(1, 21):
        user = User.objects.create_user(
            username=f"testuser{i}",
            email=f"testuser{i}@example.com",
            first_name=f"First{i}",
            last_name=f"Last{i}",
            age=20 + i  # just a sample age
        )
        user.set_password("1234")
        user.save() """
   
    pprint(connection.queries)  # Print all SQL queries executed during this run


