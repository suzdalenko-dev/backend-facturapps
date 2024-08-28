from django.db import models

class Customer(models.Model):
    id          = models.AutoField(primary_key=True)
    company_id  = models.BigIntegerField(null=True)
    usednum     = models.BigIntegerField(null=True)         

    name        = models.CharField(max_length=255, null=True)
    cif_nif     = models.CharField(max_length=33, null=True)
    address     = models.CharField(max_length=255, null=True)
    zipcode     = models.CharField(max_length=11, null=True)
    city        = models.CharField(max_length=111, null=True)
    province    = models.CharField(max_length=111, null=True)
    country     = models.CharField(max_length=111, default='España')
    phone       = models.CharField(max_length=33, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['company_id']),
        ]