# Generated by Django 5.0.2 on 2024-03-02 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_alter_business_owner'),
        ('devices', '0002_alter_device_business'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='business.business'),
        ),
    ]
