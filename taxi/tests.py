from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


class ManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 13
        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacturer_id}"
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(reverse("manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(
            len(response.context["manufacturer_list"]), 5
        )


class DriverDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        driver = Driver.objects.create(
            username="driver1", license_number="12345XYZ"
        )
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        Car.objects.create(
            model="Car1", manufacturer=manufacturer, driver=driver
        )
        Car.objects.create(
            model="Car2", manufacturer=manufacturer, driver=driver
        )

    def test_view_url_exists_at_desired_location(self):
        driver = Driver.objects.get(username="driver1")
        response = self.client.get(f"/drivers/{driver.id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        driver = Driver.objects.get(username="driver1")
        response = self.client.get(
            reverse("driver-detail", kwargs={"pk": driver.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_context_contains_cars(self):
        driver = Driver.objects.get(username="driver1")
        response = self.client.get(
            reverse("driver-detail", kwargs={"pk": driver.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("driver" in response.context)
        self.assertEqual(response.context["driver"].cars.count(), 2)
