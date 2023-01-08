from django.db import models
import uuid

class Loan(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    signed_amount = models.DecimalField(max_digits=11, decimal_places=2)
    signature_date = models.DateField()
    
    def __str__(self):
        return self.title
    
    