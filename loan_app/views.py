from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Loan
from .serializers import LoanSerializer

@api_view(['GET'])
def list_countries(request):
    countries = Loan.objects.values_list('country',flat=True)
    return Response(
        {
            "countries":countries
        }
    )
    
    
@api_view(['GET'])
def list_sectors(request):
    sectors = Loan.objects.values_list('sector',flat=True)
    return Response(
        {
            "sectors":sectors
        }
    )


@api_view(['GET'])
def list_project_titles(request):
    titles = Loan.objects.values_list('title',flat=True)
    return Response(
        {
            "project_titles":titles
        }
    )
    
class ListAllLoans(ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    