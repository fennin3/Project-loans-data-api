from rest_framework.test import APITestCase
from django.urls import reverse
import json

from loan_app.models import Loan

class TestLoanAppViews(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dataset = []
        for index in range(100):
            cls.dataset.append(
                Loan(
                    signature_date='12-04-2021',
                    title=f"Loan title {index}",
                    country=f"Country{index}",
                    sector=f"Sector{index}",
                    signed_amount=f"{100+index}"
                )
            )
        Loan.objects.bulk_create(cls.dataset)
        
    def test_list_countries_response_200(self):
        url = reverse('list_all_countries')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_list_countries_response_format_list(self):
        url = reverse('list_all_countries')
        response = self.client.get(url)
        self.assertEqual(
            json.loads(response.content)['countries'],
            [loan.country for loan in self.dataset]
        )
    
    def test_list_sectors_response_200(self):
        url = reverse('list_all_sectors')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_list_sectors_response_format_list(self):
        url = reverse('list_all_sectors')
        response = self.client.get(url)
        self.assertEqual(
            json.loads(response.content)['sectors'],
            [loan.sector for loan in self.dataset]
        )
    
    def test_list_titles_response_200(self):
        url = reverse('list_all_titles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_list_titles_response_format_list(self):
        url = reverse('list_all_titles')
        response = self.client.get(url)
        self.assertEqual(
            json.loads(response.content)['project_titles'],
            [loan.title for loan in self.dataset]
        )
    
    def test_list_loans_response_200(self):
        url = reverse('list_all_loans')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_list_loans_response_format_list(self):
        url = reverse('list_all_loans')
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content)[0]['title'], "Loan title 0")
        
        
