from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/api/v1/clubs/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "wrong"
        )
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME,)
        self.assertEqual(data[0]["description"], self.DESC,)

    def test_create_amenity(self):
        new_amenity_name = "New Amenity"
        new_amenity_description = "New amenity desc."

        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_description,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["name"],
            new_amenity_name,
        )
        self.assertEqual(
            data["description"],
            new_amenity_description,
        )

        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestAmenity(APITestCase):
    NAME = "TEST AMENITY"
    DESC = "TEST DESC"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenitiy_not_found(self):
        response = self.client.get("/api/v1/clubs/amenities/2/")

        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):
        response = self.client.get("/api/v1/clubs/amenities/1/")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["name"],
            self.NAME,
        )

        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_amenity(self):
        pass

    def test_delete_amenity(self):

        response = self.client.delete("/api/v1/clubs/amenities/1/")

        self.assertEqual(response.status_code, 204)
