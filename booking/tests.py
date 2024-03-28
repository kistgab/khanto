from datetime import date
from rest_framework.test import APITestCase
from advertisement.models import Advertisement
from booking.models import Booking
from property.models import Property


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

    def test_should_create_booking_when_everything_is_correct(self):
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
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(createdBooking)
        self.assertEqual(createdBooking.advertisement_id, data["advertisement"])
        self.assertEqual(createdBooking.check_in_date, data["check_in_date"])
        self.assertEqual(createdBooking.check_out_date, data["check_out_date"])
        self.assertEqual(createdBooking.total_guests, data["total_guests"])
        self.assertEqual(createdBooking.total_value, data["total_value"])
        self.assertEqual(createdBooking.comments, data["comments"])

    def test_should_not_create_booking_when_there_is_a_booking_in_period(
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
        self.assertEqual(response.status_code, 400)

    def test_should_not_create_booking_when_check_out_date_is_after_check_in_date(
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
        print(response.data)
        self.assertEqual(
            response.data,
            {
                "total_guests": [
                    "Total guests cannot be greater than the maximum number of guests allowed (2)"
                ]
            },
        )
