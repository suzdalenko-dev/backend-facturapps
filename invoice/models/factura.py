from django.db import models

class Factura(models.Model):
    id          = models.AutoField(primary_key=True)

    number          = models.BigIntegerField(null=True, unique=True)
    serie           = models.CharField(max_length=33, null=True)
    commercial_name = models.CharField(max_length=111, null=True)

    expiration      = models.CharField(max_length=33, null=True)
    payment_form    = models.CharField(max_length=111, default="CONTADO")
    iva             = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    base_imponible  = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    subtotal        = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    total           = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    labour_hours    = models.DecimalField(max_digits=11, decimal_places=1, null=True)

    cif         = models.CharField(max_length=33, null=True)
    exercise    = models.CharField(max_length=11, null=True)
    company_id  = models.BigIntegerField(null=True)


    class Meta:
        indexes = [
            models.Index(fields=['company_id']),
        ]