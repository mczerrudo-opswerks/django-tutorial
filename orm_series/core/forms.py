from django import forms
from core.models import Restaurant, Rating, Sales

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name','restaurant_type',)