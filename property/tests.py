import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from property.models import Property
from datetime import date

from property.serializers import PropertySerializer


# Create your tests here.
class PropertyViewTestCase(APITestCase):
    def setUp(self):
        Property.objects.create(
            max_guests=2,
            bathroom_count=2,
            accept_pets=True,
            cleaning_fee=200,
            activation_date=date.today(),
        )

    def test_should_list_all_properties_when_database_has_data(self):
        url = "/properties/"
        response = self.client.get(url)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_list_no_properties_when_database_is_empty(self):
        self.addCleanup(lambda: Property.objects.all().delete())
        self.doCleanups()
        url = "/properties/"
        response = self.client.get(url)
        self.assertEqual(response.data["count"], 0)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(response.data["results"], [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_create_property_when_everything_is_specified(self):
        url = "/properties/"
        data = {
            "max_guests": 2,
            "bathroom_count": 2,
            "accept_pets": True,
            "cleaning_fee": 200,
            "activation_date": date.today(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], 2)

    def test_should_not_create_property_when_something_is_not_specified(self):
        url = "/properties/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "max_guests": ["This field is required."],
                "bathroom_count": ["This field is required."],
                "accept_pets": ["This field is required."],
                "cleaning_fee": ["This field is required."],
                "activation_date": ["This field is required."],
            },
        )
