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


class TestRestaurantList(TestCase):
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

    def test_disallowed_methods_return_405(self):
        """
        Test that disallowed methods return a 405 status code.
        """
        for method in ("post", "put", "patch", "delete"):
            res = getattr(self.client, method)(self.url)
            self.assertEqual(res.status_code, 405)

class RestaurantCreateTests(TestCase):
    def setUp(self):
        self.url = reverse("restaurant:restaurant_create")

    def test_create_valid(self):
        payload = {
            "name": "Aroma",
            "website": "https://aroma.com",
            "date_opened": DATE,
            "latitude": 12.34,
            "longitude": 56.78,
            "address": "123 St",
            "restaurant_type": "IN",
        }
        res = jpost(self.client, self.url, payload)
        self.assertEqual(res.status_code, 201)
        out = res.json()
        self.assertIn("id", out)
        self.assertTrue(Restaurant.objects.filter(pk=out["id"], name="Aroma").exists())

    def test_create_validation_error(self):
        payload = {
            "name": "",  # required/blank invalid
            "website": "not-a-url",  # invalid URL
            "date_opened": "bad-date",  # invalid date
            "latitude": 12.34,
            "longitude": 56.78,
            "address": "123 St",
            "restaurant_type": "ZZ",  # invalid choice
        }
        res = jpost(self.client, self.url, payload)
        self.assertEqual(res.status_code, 400)
        body = res.json()
        self.assertIn("errors", body)  # from ValidationError

    def test_disallowed_methods_return_405(self):
        for method in ("get", "put", "patch", "delete"):
            http = getattr(self.client, method)
            res = http(self.url)
            self.assertEqual(res.status_code, 405)
