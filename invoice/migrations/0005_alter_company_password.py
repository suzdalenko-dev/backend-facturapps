# Generated by Django 5.1 on 2025-05-03 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_alter_company_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='password',
            field=models.CharField(max_length=222, null=True),
        ),
    ]
