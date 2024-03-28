from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from property.serializers import PropertySerializer
from property.models import Property


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

    def test_should_delete_a_property_when_the_specified_id_matches(self):
        url = "/properties/1/"
        response = self.client.delete(url)
        property_in_db = Property.objects.filter(id=1).first()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(property_in_db)

    def test_should_return_error_when_the_specified_id_dont_matches(self):
        url = "/properties/2/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": "No Property matches the given query."}
        )

    def test_should_update_property_when_everything_is_specified(self):
        property_id = 1
        url = f"/properties/{property_id}/"
        data = {
            "max_guests": 4,
            "bathroom_count": 3,
            "accept_pets": False,
            "cleaning_fee": 300,
            "activation_date": date.today(),
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], property_id)
        self.assertEqual(response.data["max_guests"], data["max_guests"])
        self.assertEqual(response.data["bathroom_count"], data["bathroom_count"])
        self.assertEqual(response.data["accept_pets"], data["accept_pets"])
        self.assertEqual(response.data["activation_date"], str(data["activation_date"]))
        self.assertEqual(Decimal(response.data["cleaning_fee"]), data["cleaning_fee"])

    def test_should_update_property_field_when_is_specified(self):
        property_id = 1
        url = f"/properties/{property_id}/"
        data = {
            "max_guests": 5,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], property_id)
        self.assertEqual(response.data["max_guests"], data["max_guests"])

    def test_should_return_error_when_updating_non_existent_field(self):
        property_id = 1
        url = f"/properties/{property_id}/"
        data = {
            "non_existent_field": 10,
        }
        property_before = Property.objects.filter(id=property_id).first()
        self.client.patch(url, data)
        property_after = Property.objects.filter(id=property_id).first()
        self.assertEqual(property_before, property_after)

    def test_should_return_error_when_updating_non_existent_property(self):
        property_id = 2
        url = f"/properties/{property_id}/"
        data = {
            "max_guests": 4,
            "bathroom_count": 3,
            "accept_pets": False,
            "cleaning_fee": 300,
            "activation_date": date.today(),
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": "No Property matches the given query."}
        )

    def test_should_retrieve_property_details_when_the_specified_id_matches(self):
        property_id = 1
        url = f"/properties/{property_id}/"
        response = self.client.get(url)
        property_in_db = Property.objects.filter(id=property_id).first()
        serializer = PropertySerializer(property_in_db)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_should_return_error_when_retrieving_details_of_nonexistent_property(self):
        property_id = 2
        url = f"/properties/{property_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": "No Property matches the given query."}
        )
