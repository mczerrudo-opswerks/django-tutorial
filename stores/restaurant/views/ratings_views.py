from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from restaurant.models import Restaurant, Rating
from django.utils import timezone
import json
from django.contrib.auth import get_user_model

User = get_user_model()

# Create Rating
@csrf_exempt # For testing purposes only, not recommended for production
def rating_create(request, restaurant_id):
    """
    Create a new rating for a restaurant
        
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            #Check if User and Restaurant exist
            user_id = data.get('user_id')
            if not user_id:
                return JsonResponse({"error": "user_id is required"}, status=400)
            user = get_object_or_404(User, pk=user_id)
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

            rating = Rating(
                user=user,
                restaurant=restaurant,
                rating=data.get('rating'),
            )
            

            rating.full_clean()  # Validate the model instance
            rating.save()
            
            return JsonResponse({'id': rating.id, 'message': 'Rating created successfully'}, status=201)

        except ValidationError as e:
            return JsonResponse({"errors": e.message_dict}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseNotAllowed(['POST'])

#Get Rating
@csrf_exempt
def rating_detail(request, rating_id):
    """
    Get details of a specific rating by its ID
        
    """
    if request.method == 'GET':
        rating = get_object_or_404(Rating, pk=rating_id)
        data = {
            'id': rating.id,
            'user_id': rating.user.id,
            'restaurant_id': rating.restaurant.id,
            'rating': rating.rating,
        }
        return JsonResponse(data, safe=True, status=200)

    return HttpResponseNotAllowed(['GET'])

# Update Rating
@csrf_exempt
def rating_update(request, rating_id):
    """
    Update an existing rating.

    """
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            rating = get_object_or_404(Rating, pk=rating_id)
            rating.rating = data.get('rating', rating.rating)

            rating.full_clean()
            rating.save()
            return JsonResponse({'message': 'Rating updated successfully'}, status=200)
        except ValidationError as e:
            return JsonResponse({"errors": e.message_dict}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseNotAllowed(['PUT'])

# Delete Rating
@csrf_exempt
def rating_delete(request, rating_id):
    """
    Delete a specific rating by its ID.
        
    """  
    if request.method == 'DELETE':
        try:
            rating = get_object_or_404(Rating, pk=rating_id)
            rating.delete()

            return JsonResponse({'message': 'Rating deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseNotAllowed(['DELETE'])


def rating_list_of_restaurant(request, restaurant_id):
    """
    List all ratings for a specific restaurant.
        
    """
    if request.method == 'GET':
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        ratings = restaurant.ratings.all().order_by('id')
        data = [
            {
                'id': rating.id,
                'user_id': rating.user.id,
                'restaurant_id': rating.restaurant.id,
                'rating': rating.rating,
            }
            for rating in ratings
        ]
        return JsonResponse(data, safe=False, status=200)

    return HttpResponseNotAllowed(['GET'])

def rating_list_of_user(request):
    """
    List all ratings for a specific user.

    """
    if request.method == 'GET':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({"error": "user_id is required"}, status=400)

        user = get_object_or_404(User, pk=user_id)
        ratings = user.ratings.all().order_by('id')
        data = [
            {
                'id': rating.id,
                'restaurant_id': rating.restaurant.id,
                'rating': rating.rating,
            }
            for rating in ratings
        ]
        return JsonResponse(data, safe=False, status=200)

    return HttpResponseNotAllowed(['GET'])

def average_rating(request, restaurant_id):
    """
    Test that a nonexistent restaurant returns a 404 error.
        
    """
    if request.method == 'GET':
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        ratings = restaurant.ratings.all()
        
        if not ratings:
            return JsonResponse({"average_rating": None}, status=200)

        average = sum(rating.rating for rating in ratings) / ratings.count()
        return JsonResponse({"average_rating": average}, status=200)

    return HttpResponseNotAllowed(['GET'])