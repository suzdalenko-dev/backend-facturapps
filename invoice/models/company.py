from django.db import models

class Company(models.Model):
    id        = models.AutoField(primary_key=True)
    cif       = models.CharField(max_length=33, null=True, unique=True)
    email     = models.CharField(max_length=111, null=True, unique=True)
    password  = models.CharField(max_length=111, null=True)
    tlf       = models.CharField(max_length=33, null=True)
    tlf2      = models.CharField(max_length=33, null=True)

    numvisit   = models.BigIntegerField(default=0)
    regtime    = models.CharField(max_length=33, null=True)
    lastvisit  = models.CharField(max_length=33, null=True)
    state      = models.CharField(max_length=22, null=True)
    uid        = models.CharField(max_length=111, null=True)

    address    = models.CharField(max_length=111, null=True)
    zipcode    = models.CharField(max_length=22, null=True)
    province   = models.CharField(max_length=11, null=True)
    country    = models.CharField(max_length=22, null=True)

    price_hour = models.DecimalField(max_digits=11, null=True, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]