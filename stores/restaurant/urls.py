from django.urls import path
from restaurant.views import restaurant_views, ratings_views

app_name = 'restaurant'
urlpatterns = [
    # Restaurant_Views
    path('restaurant/', restaurant_views.restaurant_list, name="restaurant_list"),
    path('restaurant/create/', restaurant_views.restaurant_create, name="restaurant_create"),
    path('restaurant/<int:restaurant_id>/', restaurant_views.restaurant_detail, name="restaurant_detail"),
    path('restaurant/<int:restaurant_id>/update/', restaurant_views.restaurant_update, name="restaurant_update"),
    path('restaurant/<int:restaurant_id>/delete/', restaurant_views.restaurant_delete, name="restaurant_delete"),

    # Ratings_Views
    path('restaurant/<int:restaurant_id>/ratings/', ratings_views.rating_list_of_restaurant, name="ratings_list"),
    path('restaurant/<int:restaurant_id>/ratings/create/', ratings_views.rating_create, name="rating_create"),
    path('ratings/<int:rating_id>/', ratings_views.rating_detail, name="rating_detail"),
    path('ratings/<int:rating_id>/update/', ratings_views.rating_update, name="rating_update"),
    path('ratings/<int:rating_id>/delete/', ratings_views.rating_delete, name="rating_delete"),
    path('user/ratings/', ratings_views.rating_list_of_user, name="user_ratings"),
    path('restaurant/<int:restaurant_id>/average-rating/', ratings_views.average_rating, name="average_rating"),

]