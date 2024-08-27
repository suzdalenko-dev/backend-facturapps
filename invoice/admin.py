from django.contrib import admin
from .models.company import Company
from .models.country import Country

# Register your models here.

admin.site.register(Company)
admin.site.register(Country)