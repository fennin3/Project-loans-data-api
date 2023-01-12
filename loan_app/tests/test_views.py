from rest_framework.test import APITestCase
from django.urls import reverse
import json

from loan_app.models import Loan, Country, Sector, Currency


class TestLoanAppViews(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = Country.objects.create(name=f"USA")
        cls.currency = Currency.objects.create(symbol="$")
        cls.sector = Sector.objects.create(name="Health")
        cls.dataset = []
        for index in range(100):
            cls.dataset.append(
                Loan(
                    signature_date="2021-12-04",
                    title=f"Loan title {index}",
                    country=cls.country,
                    currency=cls.currency,
                    sector=cls.sector,
                    signed_amount=f"{100+index}",
                )
            )
        Loan.objects.bulk_create(cls.dataset)

    def test_list_countries_response_200(self):
        url = reverse("list_all_countries")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_countries_response_format_list(self):
        url = reverse("list_all_countries")
        response = self.client.get(url)
        self.assertEqual(
            json.loads(response.content)["countries"][0],
            self.country.name,
        )

    def test_list_sectors_response_200(self):
        url = reverse("list_all_sectors")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_sectors_response_format_list(self):
        url = reverse("list_all_sectors")
        response = self.client.get(url)
        self.assertEqual(
            json.loads(response.content)["sectors"][0],
            self.sector.name,
        )

    def test_list_titles_response_200(self):
        url = reverse("list_all_titles")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_titles_response_format_list(self):
        url = reverse("list_all_titles")
        response = self.client.get(url)
        self.assertEqual(
            json.loads(response.content)["project_titles"],
            [loan.title for loan in self.dataset],
        )

    def test_list_loans_response_200(self):
        url = reverse("list_all_loans")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_loans_response_format_list(self):
        url = reverse("list_all_loans")
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content)[0]["title"], "Loan title 0")

    def test_excel_generation_response_200(self):
        url = reverse("generate_excel")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
