from django.urls import path

from . import views

urlpatterns = [
    path("countries", views.list_countries, name="list_all_countries"),
    path("sectors", views.list_sectors, name="list_all_sectors"),
    path("projects", views.list_project_titles, name="list_all_titles"),
    path("loans", views.ListAllLoans.as_view(), name="list_all_loans"),
    path("excel", views.generate_excel_records, name="generate_excel"),
]
