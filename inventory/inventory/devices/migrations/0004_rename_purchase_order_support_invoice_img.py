# Generated by Django 5.0.2 on 2024-03-03 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_alter_device_business'),
    ]

    operations = [
        migrations.RenameField(
            model_name='support',
            old_name='purchase_order',
            new_name='invoice_img',
        ),
    ]