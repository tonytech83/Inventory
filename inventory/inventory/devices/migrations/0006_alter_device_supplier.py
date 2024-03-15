# Generated by Django 5.0.2 on 2024-03-15 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_alter_device_building'),
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='suppliers.supplier'),
        ),
    ]
