from rest_framework.serializers import ModelSerializer

from .models import Loan

class LoanSerializer(ModelSerializer):
    class Meta:
        model=Loan
        fields="__all__"