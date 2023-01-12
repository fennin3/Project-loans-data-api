from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import HttpResponse
from django.db.models import Sum, Count, Avg

from .models import Loan, Sector, Country
from .serializers import LoanSerializer
from .utils import generate_excel


@api_view(["GET"])
def list_countries(request):
    countries = Country.objects.values_list("name", flat=True)
    return Response({"countries": countries})


@api_view(["GET"])
def list_sectors(request):
    sectors = Sector.objects.values_list("name", flat=True)
    return Response({"sectors": sectors})


@api_view(["GET"])
def list_project_titles(request):
    titles = Loan.objects.values_list("title", flat=True)
    return Response({"project_titles": titles})


class ListAllLoans(ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


@api_view(["GET"])
def generate_excel_records(request):
    # generating excel record
    dataset = Loan.objects.select_related("country", "sector", "currency").all()

    by_year = dataset.values("signature_date__year").annotate(
        total_amount=Sum("signed_amount"),
        count=Count("uid"),
    )

    by_country = dataset.values("country__name").annotate(
        total_amount=Sum("signed_amount"),
        count=Count("uid"),
    )

    by_sector = dataset.values("sector__name").annotate(
        total_amount=Sum("signed_amount"),
        count=Count("uid"),
    )

    excel_output = generate_excel(dataset, by_year, by_country, by_sector)

    # print(query)
    # Set up the Http response.
    filename = "loan_data.xlsx"
    response = HttpResponse(
        excel_output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response
