from django.db import models

class Article(models.Model):
    id          = models.AutoField(primary_key=True)
    company_id  = models.BigIntegerField(null=True)
    usenum      = models.BigIntegerField(null=True)

    code        = models.CharField(max_length=41, null=True, unique=True)
    description = models.CharField(max_length=111, null=True, unique=True)
    quantity    = models.DecimalField(max_digits=11, null=True, decimal_places=2)
    price       = models.DecimalField(max_digits=11, null=True, decimal_places=2)


    class Meta:
        indexes = [
            models.Index(fields=['company_id']),
        ]