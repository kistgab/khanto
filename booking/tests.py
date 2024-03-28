from datetime import date
from rest_framework.test import APITestCase
from advertisement.models import Advertisement
from booking.models import Booking
from booking.serializers import BookingSerializer
from property.models import Property
from rest_framework import status


class BookingViewTestCase(APITestCase):
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
        Booking.objects.create(
            advertisement_id=1,
            check_in_date=date.fromisoformat("2021-09-01"),
            check_out_date=date.fromisoformat("2021-09-03"),
            total_guests=2,
            total_value=240,
            comments="comments",
        )

    def test_should_create_booking_correctly(self):
        url = "/bookings/"
        data = {
            "advertisement": 1,
            "check_in_date": date.fromisoformat("2021-09-04"),
            "check_out_date": date.fromisoformat("2021-09-10"),
            "total_guests": 2,
            "total_value": 240,
            "comments": "comments",
        }
        response = self.client.post(url, data)
        createdBooking = Booking.objects.get(id=response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(createdBooking)
        self.assertEqual(createdBooking.advertisement_id, data["advertisement"])
        self.assertEqual(createdBooking.check_in_date, data["check_in_date"])
        self.assertEqual(createdBooking.check_out_date, data["check_out_date"])
        self.assertEqual(createdBooking.total_guests, data["total_guests"])
        self.assertEqual(createdBooking.total_value, data["total_value"])
        self.assertEqual(createdBooking.comments, data["comments"])

    def test_should_not_create_booking_when_there_is_already_a_booking_in_specified_period(
        self,
    ):
        url = "/bookings/"
        data = {
            "advertisement": 1,
            "check_in_date": date.fromisoformat("2021-09-02"),
            "check_out_date": date.fromisoformat("2021-09-05"),
            "total_guests": 2,
            "total_value": 240,
            "comments": "comments",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_create_booking_when_checkout_date_is_after_checkin_date(
        self,
    ):
        url = "/bookings/"
        data = {
            "advertisement": 1,
            "check_in_date": date.fromisoformat("2021-09-10"),
            "check_out_date": date.fromisoformat("2021-09-08"),
            "total_guests": 2,
            "total_value": 240,
            "comments": "comments",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"check_out_date": ["Check-out date cannot be before than Check-in date"]},
        )

    def test_should_not_create_booking_when_total_guests_are_more_than_allowed(
        self,
    ):
        url = "/bookings/"
        data = {
            "advertisement": 1,
            "check_in_date": date.fromisoformat("2021-09-10"),
            "check_out_date": date.fromisoformat("2021-09-15"),
            "total_guests": 55555,
            "total_value": 240,
            "comments": "comments",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "total_guests": [
                    "Total guests cannot be greater than the maximum number of guests allowed (2)"
                ]
            },
        )

    def test_should_list_all_bookings(self):
        url = "/bookings/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0],
            BookingSerializer(Booking.objects.all().first()).data,
        )

    def test_should_list_no_bookings_when_database_is_empty(self):
        self.addCleanup(lambda: Advertisement.objects.all().delete())
        self.doCleanups()
        url = "/bookings/"
        response = self.client.get(url)
        self.assertEqual(response.data["count"], 0)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(response.data["results"], [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_retrieve_booking_by_id(self):
        booking = Booking.objects.first()
        url = f"/bookings/{booking.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, BookingSerializer(booking).data)

    def test_should_not_retrieve_booking_when_specified_id_doesnt_exist(
        self,
    ):
        url = "/bookings/1234/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": "No Booking matches the given query."}
        )

    def test_should_delete_booking_by_id(self):
        booking_id = Booking.objects.first().id
        url = f"/bookings/{booking_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Booking.objects.filter(id=booking_id).exists())

    def test_should_not_delete_booking_when_specified_id_doesnt_exist(self):
        booking_id = 1234
        url = f"/bookings/{booking_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": "No Booking matches the given query."}
        )
