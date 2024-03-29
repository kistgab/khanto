from datetime import date
from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework import status
from advertisement.models import Advertisement
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
        Advertisement.objects.create(
            property_id=1, platform_name="platform_name", platform_fee=40
        )

    def test_should_list_all_advertisements(self):
        url = "/advertisements/"
        response = self.client.get(url)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_list_no_advertisements_when_database_is_empty(self):
        self.addCleanup(lambda: Advertisement.objects.all().delete())
        self.doCleanups()
        url = "/advertisements/"
        response = self.client.get(url)
        self.assertEqual(response.data["count"], 0)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(response.data["results"], [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_create_advertisement_correctly(self):
        url = "/advertisements/"
        data = {
            "property": 1,
            "platform_name": "platform_name",
            "platform_fee": 40,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], 2)

    def test_should_not_create_advertisement_when_something_is_not_specified(self):
        url = "/advertisements/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "platform_name": ["This field is required."],
                "platform_fee": ["This field is required."],
                "property": ["This field is required."],
            },
        )

    def test_should_not_permit_to_delete_an_advertisement(self):
        url = "/advertisements/1/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_should_update_all_advertisement_fields(self):
        url = "/advertisements/1/"
        data = {
            "property": 1,
            "platform_name": "new_platform_name",
            "platform_fee": 50.00,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["platform_name"], "new_platform_name")
        self.assertEqual(Decimal(response.data["platform_fee"]), 50)

    def test_should_update_some_advertisement_fields(self):
        url = "/advertisements/1/"
        data = {
            "platform_name": "new_platform_name",
        }
        response = self.client.patch(url, data)
        advertisement_after = Advertisement.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["platform_name"], "new_platform_name")
        self.assertEqual(advertisement_after.platform_name, "new_platform_name")

    def test_should_retrieve_advertisement_by_id(self):
        url = "/advertisements/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["platform_name"], "platform_name")
        self.assertEqual(Decimal(response.data["platform_fee"]), 40)
        self.assertEqual(response.data["property_info"]["id"], 1)

    def test_should_not_retrieve_advertisement_when_specified_id_doesnt_exist(
        self,
    ):
        url = "/advertisements/1234/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": "No Advertisement matches the given query."}
        )
