from django.db import models

class Company(models.Model):
    id        = models.AutoField(primary_key=True)
    cif       = models.CharField(max_length=33, null=True, unique=True)
    email     = models.CharField(max_length=111, null=True, unique=True)
    password  = models.CharField(max_length=111, null=True)
    tlf       = models.CharField(max_length=33, null=True)

    numvisit  = models.BigIntegerField(default=0)
    lastvisit = models.CharField(max_length=33, null=True)
    state     = models.CharField(max_length=22, null=True)
    hascode   = models.CharField(max_length=111, null=True)

    address   = models.CharField(max_length=111, null=True)
    zipcode   = models.CharField(max_length=22, null=True)
    province  = models.CharField(max_length=11, null=True)
    country   = models.CharField(max_length=22, null=True)


    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]