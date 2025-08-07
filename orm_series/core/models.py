from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Create your models here.
# User model
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

UserModel = get_user_model()


# Custom Validation 
def validate_restaurant_name_begins_with_a(value):
    if not value.startswith('a'):
        raise ValidationError(
            f'{value} does not start with "A". Please enter a valid restaurant name.'
        )


# Restaurant model
class Restaurant(models.Model):
    class TypeChoices(models.TextChoices):
        INDIAN = 'IN', 'Indian'
        CHINESE = 'CH', 'Chinese'
        ITALIAN = 'IT', 'Italian'
        MEXICAN = 'MX', 'Mexican'
        AMERICAN = 'AM', 'American'
        FILIPINO = 'PH', 'Filipino'
        OTHER = 'OT', 'Other'

    name = models.CharField(max_length=100, validators=[validate_restaurant_name_begins_with_a])
    website = models.URLField(default='')
    date_opened = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)
    restaurant_type = models.CharField(max_length=2, choices=TypeChoices.choices, default=TypeChoices.OTHER )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
       print(self._state.adding)
       super().save(*args, **kwargs)


    
# Rating model
class Rating(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1
    )

    def __str__(self):
        return f"Rating: {self.rating}"
    
# Sales model
class Sales(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name='sales')
    income = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField()

    def __str__(self):
        return f"Sales for {self.restaurant.name} on {self.datetime}: ${self.income}"

