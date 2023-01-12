from rest_framework.serializers import ModelSerializer
from .models import Loan, Country, Sector, Currency


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ("name",)


class SectorSerializer(ModelSerializer):
    class Meta:
        model = Sector
        fields = ("name",)


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = ("symbol",)


class LoanSerializer(ModelSerializer):
    country = CountrySerializer()
    sector = SectorSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Loan
        fields = (
            "uid",
            "title",
            "signed_amount",
            "signature_date",
            "country",
            "sector",
            "currency",
        )
