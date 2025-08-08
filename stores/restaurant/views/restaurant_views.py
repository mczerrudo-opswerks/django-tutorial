from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from restaurant.models import Restaurant
from django.utils import timezone
import json
# Create your views here.

def restaurant_list(request):
    if request.method == 'GET':
        restaurants = Restaurant.objects.all().order_by('id')
        data = {
            'restaurants': [
                {
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'website': restaurant.website,
                    'date_opened': restaurant.date_opened,
                    'latitude': restaurant.latitude,
                    'longitude': restaurant.longitude,
                    'address': restaurant.address,
                    'restaurant_type': restaurant.restaurant_type
                } for restaurant in restaurants
            ]
        }
        return JsonResponse(data, safe=False, status=200)

    return HttpResponseNotAllowed(['GET'])


@csrf_exempt # For testing purposes only, not recommended for production
def restaurant_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            restaurant = Restaurant(
                name=data.get('name'),
                website=data.get('website'),
                date_opened=data.get('date_opened'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                address=data.get('address'),
                restaurant_type=data.get('restaurant_type')
            )

            restaurant.full_clean()  # Validate the model instance
            restaurant.save()
            return JsonResponse({'id': restaurant.id, 'message': 'Restaurant created successfully'}, status=201)
        
        except ValidationError as e:
            return JsonResponse({"errors": e.message_dict}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def restaurant_detail(request, restaurant_id):
    if request.method == 'GET':
        try:
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
            data = {
                'id': restaurant.id,
                'name': restaurant.name,
                'website': restaurant.website,
                'date_opened': restaurant.date_opened,
                'latitude': restaurant.latitude,
                'longitude': restaurant.longitude,
                'address': restaurant.address,
                'restaurant_type': restaurant.restaurant_type
            }
            return JsonResponse(data, safe=True, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"error": "Restaurant not found"}, status=404)

    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def restaurant_update(request, restaurant_id):
    if request.method == 'PUT':
        try:
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
            data = json.loads(request.body)
            restaurant.name = data.get('name', restaurant.name)
            restaurant.website = data.get('website', restaurant.website)
            restaurant.date_opened = data.get('date_opened', restaurant.date_opened)
            restaurant.latitude = data.get('latitude', restaurant.latitude)
            restaurant.longitude = data.get('longitude', restaurant.longitude)
            restaurant.address = data.get('address', restaurant.address)
            restaurant.restaurant_type = data.get('restaurant_type', restaurant.restaurant_type)
            restaurant.full_clean()  # Validate the model instance
            restaurant.save()

            return JsonResponse({'id': restaurant.id, 'message': 'Restaurant updated successfully'}, status=200)

        except ValidationError as e:
            return JsonResponse({"errors": e.message_dict}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseNotAllowed(['PUT'])

@csrf_exempt
def restaurant_delete(request, restaurant_id):
    if request.method == 'DELETE':
        try:
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
            restaurant.delete()
            return JsonResponse({'message': 'Restaurant deleted successfully'}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseNotAllowed(['DELETE'])


