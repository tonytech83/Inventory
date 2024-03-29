# Generated by Django 5.0.3 on 2024-03-28 19:41

import django.core.validators
import inventory.core.model_validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('supplier_country', models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(3)])),
                ('contact_name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(6)])),
                ('phone_number', models.CharField(max_length=15, validators=[inventory.core.model_validators.phone_validator])),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
