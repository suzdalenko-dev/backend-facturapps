from django.db import models

class Vehicledata(models.Model):
    id           = models.AutoField(primary_key=True)
    invoice_id   = models.BigIntegerField(null=True)
    company_id   = models.BigIntegerField(null=True)
    customer_id  = models.BigIntegerField(null=True)

    registration   = models.CharField(max_length=11, null=True)   # matricula
    colour         = models.CharField(max_length=22, null=True)   # color
    kilometres     = models.PositiveIntegerField(null=True)       # km
    make           = models.CharField(max_length=111, null=True)  # marca
    model          = models.CharField(max_length=111, null=True)  # modelo
    chassis_number = models.CharField(max_length=111, null=True)  # numero chasis