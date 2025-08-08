from django.urls import path
from . import views

app_name = 'restaurant'
urlpatterns = [
    path('', views.restaurant_list, name="list"),
    path('create/', views.restaurant_create, name="create"),
    path('<int:pk>/', views.restaurant_detail, name="detail"),
    path('<int:pk>/update/', views.restaurant_update, name="update"),
]