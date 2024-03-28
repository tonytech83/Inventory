# Generated by Django 5.0.3 on 2024-03-28 13:23

import inventory.core.model_validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[inventory.core.model_validators.phone_validator]),
        ),
    ]
