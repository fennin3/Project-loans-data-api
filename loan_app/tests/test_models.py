from django.test import TestCase
from loan_app.models import Loan

class TestLoanAppModels(TestCase):
    
    def test_loan_model_fields(self):
        test_loan = Loan.objects.create(
            signature_date='12-04-2021',
            title=f"Loan Title atm",
            country=f"Germany",
            sector=f"Sector ABC",
            signed_amount="3509"
        )
        
        load = Loan.objects.first()
        
        self.assertEqual(load.title,test_loan.title)
        self.assertEqual(load.sector,test_loan.sector)
        self.assertEqual(load.country,test_loan.country)
        self.assertEqual(load.signature_date,test_loan.signature_date)
        self.assertEqual(load.signed_amount,test_loan.signed_amount)
        