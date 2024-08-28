from django.db import models

class Factura(models.Model):
    id               = models.AutoField(primary_key=True)
    numero           = models.BigIntegerField(null=True, unique=True)
    serie            = models.CharField(max_length=33, null=True)
    nombre_cliente   = models.CharField(max_length=111, null=True)
    cif              = models.CharField(max_length=33, null=True)
    ejercicio        = models.CharField(max_length=11, null=True)
    company_id       = models.BigIntegerField(null=True)

    fecha            = models.CharField(max_length=33, null=True)
    vencimiento      = models.CharField(max_length=33, null=True)
    forma_pago       = models.CharField(max_length=111, default="CONTADO")
    
    baseimponible1   = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    baseimponible2   = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    baseimponible3   = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    baseimponible4   = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    baseimponible5   = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    iva1             = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    iva2             = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    iva3             = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    iva4             = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    iva5             = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importeiva1      = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importeiva2      = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importeiva3      = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importeiva4      = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importeiva5      = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    totaliva         = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    recargo1         = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    recargo2         = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    recargo3         = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    recargo4         = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    recargo5         = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importerecargo1  = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importerecargo2  = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importerecargo3  = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importerecargo4  = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    importerecargo5  = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    totalivarecargo  = models.DecimalField(max_digits=11, decimal_places=2, default=0)
   
   
    base_imponible   = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    subtotal         = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    total            = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    labour_hours    = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    


    class Meta:
        indexes = [
            models.Index(fields=['company_id']),
        ]