from django.test import SimpleTestCase
from django.urls import reverse, resolve

from loan_app import views


class TestLoanAppURLS(SimpleTestCase):
    def test_list_countries_resolves(self):
        url = reverse("list_all_countries")
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.list_countries)

    def test_list_sectors_resolves(self):
        url = reverse("list_all_sectors")
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.list_sectors)

    def test_list_titles_resolves(self):
        url = reverse("list_all_titles")
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.list_project_titles)

    def test_list_all_loans_resolves(self):
        url = reverse("list_all_loans")
        url_view_function = resolve(url).func.view_class
        self.assertEqual(url_view_function, views.ListAllLoans)
