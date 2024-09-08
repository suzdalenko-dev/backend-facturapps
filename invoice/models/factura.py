from django.db import models

class Factura(models.Model):
    id                    = models.AutoField(primary_key=True)
    company_id            = models.BigIntegerField(null=True)
    tipo_factura          = models.CharField(max_length=3, null=True)
    ejercicio             = models.CharField(max_length=7, null=True)
    serie_fact            = models.CharField(max_length=22, null=True)
    numero                = models.BigIntegerField(null=True)                           
    serie_fact_unique     = models.CharField(max_length=22, null=True, unique=True)

    customer_id           = models.BigIntegerField(null=True)
                                                                                        # 1.Número de factura y, en su caso, serie.
    
    fecha_expedicion      = models.CharField(max_length=33, null=True)                  # 2.Fecha de expedición.
    fecha_efecto          = models.CharField(max_length=33, null=True)
            
    receptor_cif          = models.CharField(max_length=33, null=True)                  # 3.Nombre y apellidos, razón o denominación social tanto del emisor como del receptor de la factura.
    receptor_company_name = models.CharField(max_length=111, null=True)
    receptor_person_name  = models.CharField(max_length=111, null=True)
    receptor_pais         = models.CharField(max_length=111, null=True)
    receptor_zip_code     = models.CharField(max_length=111, null=True)
    receptor_city         = models.CharField(max_length=111, null=True)
    receptor_address      = models.CharField(max_length=111, null=True)                 
    emisor_cif            = models.CharField(max_length=33, null=True)
    emisor_company_name   = models.CharField(max_length=111, null=True)                 # 4. Número de identificación fiscal (NIF) de ambas partes.
    emisor_person_name    = models.CharField(max_length=111, null=True)                 # 5. Domicilio del emisor y del receptor.
    emisor_pais           = models.CharField(max_length=111, null=True)                 # 6. Descripción de las operaciones para determinar la base imponible del impuesto.
    emisor_zip_code       = models.CharField(max_length=111, null=True)                 # 7. Precio unitario de las operaciones. Es decir, sin incluir impuestos.
    emisor_provice        = models.CharField(max_length=111, null=True)
    emisor_city           = models.CharField(max_length=111, null=True)                 # 8. El tipo impositivo que se aplica, así como la cuota tributaria.
    emisor_address        = models.CharField(max_length=111, null=True)                 # 9. La fecha en la que se hayan efectuado las operaciones siempre que se trate de una fecha distinta a la de expedición de la factura.

    
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

    labour_hours     = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    observacion      = models.CharField(max_length=254, null=True)
    comentario      = models.CharField(max_length=254, null=True)
    


    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['company_id']),
        ]