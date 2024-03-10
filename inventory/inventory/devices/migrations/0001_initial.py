# Generated by Django 5.0.2 on 2024-03-10 06:58

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
        ('suppliers', '0001_initial'),
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
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_order_number', models.IntegerField(blank=True, null=True)),
                ('invoice_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('sos', models.DateField()),
                ('eos', models.DateField()),
                ('eol', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('domain', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(1)])),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('In operation', 'In operation'), ('Retired', 'Retired'), ('Pending Setup', 'Pending Setup'), ('Offline', 'Offline'), ('Not defined yet', 'Not defined yet'), ('Exception', 'Exception')], default='Not defined yet', max_length=20)),
                ('category', models.CharField(choices=[('Network', 'Network'), ('Server - Virtual', 'Server - Virtual'), ('Server - Physical', 'Server - Physical'), ('Server - Platform', 'Server - Platform'), ('Printer/Scanner', 'Printer/Scanner'), ('Storage', 'Storage'), ('Conferencing', 'Conferencing'), ('End Users Computing', 'End Users Computing'), ('AirCon', 'AirCon'), ('UPS', 'UPS'), ('Other', 'Other')], default='Other', max_length=50)),
                ('sub_category', models.CharField(choices=[('Router', 'Router'), ('Firewall', 'Firewall'), ('Firewall/IDS/IPS', 'Firewall/IDS/IPS'), ('Access Point', 'Access Point'), ('Switch', 'Switch'), ('Desktop', 'Desktop'), ('Laptop', 'Laptop'), ('Printer/MFP', 'Printer/MFP'), ('Scanner', 'Scanner'), ('IP Phone', 'IP Phone'), ('Teleconferencing/Modem', 'Teleconferencing/Modem'), ('VoIP System - Cisco CM', 'VoIP System - Cisco CM'), ('VoIP System - other', 'VoIP System - other'), ('App and DB Server', 'App and DB Server'), ('Application Server', 'Application Server'), ('Database Server', 'Database Server'), ('File Server', 'File Server'), ('Other Server', 'Other Server'), ('Backup device', 'Backup device'), ('Storage - NAS', 'Storage - NAS'), ('Storage - SAN', 'Storage - SAN'), ('Data Historian', 'Data Historian'), ('Human Machine Interface (HMI)', 'Human Machine Interface (HMI)'), ('IDS/IPS Detection', 'IDS/IPS Detection'), ('Master Terminal Unit (MTU)', 'Master Terminal Unit (MTU)'), ('Programmable Logic Controller (PLC)', 'Programmable Logic Controller (PLC)'), ('Remote Access', 'Remote Access'), ('Remote Terminal Unit (RTU)', 'Remote Terminal Unit (RTU)'), ('Other hardware', 'Other hardware')], default='Other hardware', max_length=50)),
                ('manufacturer', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1)])),
                ('model', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1)])),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, unique=True)),
                ('ip_address_sec', models.GenericIPAddressField(blank=True, null=True, unique=True)),
                ('serial_number', models.CharField(blank=True, max_length=30, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('operating_system', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('owner_name', models.CharField(default='Unknown', max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='business.business')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='suppliers.supplier')),
                ('risk', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='devices.risk')),
                ('support', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='devices.support')),
            ],
        ),
    ]
