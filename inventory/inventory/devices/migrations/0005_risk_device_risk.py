# Generated by Django 5.0.2 on 2024-03-03 06:39

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_rename_purchase_order_support_invoice_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('support_model', models.TextField(help_text='Short description of support model', max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('business_processes_at_risk', models.TextField(help_text='Identify the business process that is at risk', max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('impact', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('likelihood', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='risk',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='devices.risk'),
        ),
    ]