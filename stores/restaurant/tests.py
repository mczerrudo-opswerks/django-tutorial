import json
from django.test import TestCase
from django.urls import reverse
from restaurant.models import Restaurant
from django.utils import timezone

DATE = "2024-01-02"  

# Helper functions for JSON requests
def jpost(client, url, payload):
    return client.post(url, data=json.dumps(payload), content_type="application/json")

def jput(client, url, payload):
    return client.put(url, data=json.dumps(payload), content_type="application/json")


class RestaurantListTests(TestCase):
    def setUp(self):
        self.r1 = Restaurant.objects.create(
            name="B", website="https://b.com", date_opened="2023-01-01",
            latitude=1.0, longitude=1.0, address="addr B", restaurant_type="IN"
        )
        self.r0 = Restaurant.objects.create(
            name="A", website="https://a.com", date_opened="2022-01-01",
            latitude=0.0, longitude=0.0, address="addr A", restaurant_type="IN"
        )
        self.url = reverse("restaurant:restaurant_list")

    def test_get_returns_restaurants_sorted_by_id(self):
        """
        Test that the restaurant list is returned sorted by ID in ascending order.
        """
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        ids = [item["id"] for item in res.json()["restaurants"]]
        self.assertEqual(ids, sorted(ids))

class RestaurantCreateTests(TestCase):
    def setUp(self):
        self.url = reverse("restaurant:restaurant_create")

    def test_create_valid(self):
        """
        Test that a valid restaurant can be created
        
        """
        data = {
            "name": "Aroma",
            "website": "https://aroma.com",
            "date_opened": DATE,
            "latitude": 12.34,
            "longitude": 56.78,
            "address": "123 St",
            "restaurant_type": "IN",
        }
        res = jpost(self.client, self.url, data)
        self.assertEqual(res.status_code, 201)
        out = res.json()
        self.assertIn("id", out)
        self.assertTrue(Restaurant.objects.filter(pk=out["id"], name="Aroma").exists())

    def test_create_validation_error(self):
        """
        Test that a restaurant cannot be created with invalid data.

        """
        data = {
            "name": "",  # required/blank invalid
            "website": "not-a-url",  
            "date_opened": "bad-date",  # invalid date
            "latitude": 12.34,
            "longitude": 56.78,
            "address": "123 St",
            "restaurant_type": "ZZ",  # invalid choice
        }
        res = jpost(self.client, self.url, data)
        self.assertEqual(res.status_code, 400)
        body = res.json()
        self.assertIn("errors", body)  # from ValidationError
        self.assertEqual(res.status_code, 400)

class RestaurantDetailTests(TestCase):
    def setUp(self):
        self.r0 = Restaurant.objects.create(
            name="A", website="https://a.com", date_opened="2022-01-01",
            latitude=0.0, longitude=0.0, address="addr A", restaurant_type="OH"
        )
        self.r1 = Restaurant.objects.create(
            name="B", website="https://b.com", date_opened="2023-01-01",
            latitude=1.0, longitude=1.0, address="addr B", restaurant_type="IN"
        )
        self.url = reverse("restaurant:restaurant_detail", kwargs={"restaurant_id": self.r1.id})
    
    def test_get_returns_restaurant_details(self):
        """
        Test that the restaurant details are returned correctly.

        """
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["id"], self.r1.id)
        self.assertEqual(data["name"], self.r1.name)
        self.assertEqual(data["website"], self.r1.website)
        self.assertEqual(data["date_opened"], str(self.r1.date_opened))
        self.assertEqual(data["latitude"], self.r1.latitude)
        self.assertEqual(data["longitude"], self.r1.longitude)
        self.assertEqual(data["address"], self.r1.address)
        self.assertEqual(data["restaurant_type"], self.r1.restaurant_type)

    def test_get_nonexistent_restaurant_returns_404(self):
        """
        Test that a nonexistent restaurant returns a 404 error.
        """
        url = reverse("restaurant:restaurant_detail", kwargs={"restaurant_id": 999})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)
