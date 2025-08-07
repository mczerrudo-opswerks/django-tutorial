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

    rating =Rating.objects.create(
        user=user,
        restaurant=restaurant,
        rating=0
    )

    rating.full_clean()  # Validate the model instance
    rating.save()  # Save the instance to the database

    pprint(connection.queries)  # Print all SQL queries executed during this run


