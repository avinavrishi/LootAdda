# Generated by Django 3.2.5 on 2023-02-27 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20230206_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawal',
            name='account_holder_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='withdrawal',
            name='account_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
