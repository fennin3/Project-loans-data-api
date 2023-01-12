from django.test import TestCase
from loan_app.models import Loan, Country, Sector, Currency

from decimal import Decimal


class TestLoanAppModels(TestCase):
    def test_loan_model_fields(self):
        country = Country.objects.create(name=f"USA")
        currency = Currency.objects.create(symbol="$")
        sector = Sector.objects.create(name="Health")
        test_loan = Loan.objects.create(
            signature_date="2021-12-04",
            title=f"Loan Title atm",
            country=country,
            sector=sector,
            currency=currency,
            signed_amount="3509",
        )

        loan = Loan.objects.first()

        self.assertEqual(loan.title, test_loan.title)
        self.assertEqual(loan.sector, sector)
        self.assertEqual(loan.country, country)
        self.assertEqual(loan.signed_amount, Decimal(test_loan.signed_amount))
