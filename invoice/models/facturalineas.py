from django.db import models

class Facturalineas(models.Model):
    id           = models.AutoField(primary_key=True)
    invoice_id   = models.BigIntegerField(null=True)
    company_id   = models.BigIntegerField(null=True)

    article_id   = models.BigIntegerField(null=True)
    article_name = models.CharField(max_length=111, null=True)
    quantity     = models.PositiveIntegerField()
    unit_price   = models.DecimalField(max_digits=11, decimal_places=2)
    amount       = models.DecimalField(max_digits=11, decimal_places=2)


    class Meta:
        indexes = [
            models.Index(fields=['company_id']),
            models.Index(fields=['invoice_id']),
        ]