from django.db import models

class Document(models.Model):
    id          = models.AutoField(primary_key=True)
    description = models.CharField(max_length=41, unique=True, null=True)
    value       = models.PositiveIntegerField(default=0)

    company_id  = models.BigIntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['description']),
            models.Index(fields=['company_id']),
        ]