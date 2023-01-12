from django.contrib import admin
from .models import Loan, Country, Currency, Sector

admin.site.register(Loan)
admin.site.register(Country)
admin.site.register(Currency)
admin.site.register(Sector)
