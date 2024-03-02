from django.core.validators import MinLengthValidator
from django.db import models
from datetime import datetime
from inventory.business.models import Business
from inventory.suppliers.models import Supplier


class OperationSystem(models.Model):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 30

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
        ),
    )


class Support(models.Model):
    """
    warranty -> how many years

    """
    purchase_order_number = models.IntegerField(
        # TODO: to validate length of PO ?
        null=True,
        blank=True,
    )

    purchase_order = models.ImageField(
        # TODO: To fix upload of pdf document or pic maybe
        null=True,
        blank=True,
    )

    sos = models.DateField()

    eos = models.DateField()

    eol = models.DateField()

    @property
    def days_under_support(self):
        return datetime.now().date() - self.eos


class Category(models.TextChoices):
    NETWORK = 'Network', 'Network'
    SERVER_VIRTUAL = 'Server - Virtual', 'Server - Virtual'
    SERVER_PHYSICAL = 'Server - Physical', 'Server - Physical'
    SERVER_PLATFORM = 'Server - Platform', 'Server - Platform'
    PRINTER_SCANNER = 'Printer/Scanner', 'Printer/Scanner'
    STORAGE = 'Storage', 'Storage'
    CONFERENCING = 'Conferencing', 'Conferencing'
    END_USERS_COMPUTING = 'End Users Computing', 'End Users Computing'
    AIRCON = 'AirCon', 'AirCon'
    UPS = 'UPS', 'UPS'
    OTHER = 'Other', 'Other'


class SubCategory(models.TextChoices):
    ROUTER = 'Router', 'Router'
    FIREWALL = 'Firewall', 'Firewall'
    FIREWALL_IDS_IPS = 'Firewall/IDS/IPS', 'Firewall/IDS/IPS'
    ACCESS_POINT = 'Access Point', 'Access Point'
    SWITCH = 'Switch', 'Switch'
    DESKTOP = 'Desktop', 'Desktop'
    LAPTOP = 'Laptop', 'Laptop'
    PRINTER_MFP = 'Printer/MFP', 'Printer/MFP'
    SCANNER = 'Scanner', 'Scanner'
    IP_PHONE = 'IP Phone', 'IP Phone'
    TELECONFERENCING_MODEM = 'Teleconferencing/Modem', 'Teleconferencing/Modem'
    VOIP_SYSTEM_CISCO_CM = 'VoIP System - Cisco CM', 'VoIP System - Cisco CM'
    VOIP_SYSTEM_OTHER = 'VoIP System - other', 'VoIP System - other'
    APP_AND_DB_SERVER = 'App and DB Server', 'App and DB Server'
    APPLICATION_SERVER = 'Application Server', 'Application Server'
    DATABASE_SERVER = 'Database Server', 'Database Server'
    FILE_SERVER = 'File Server', 'File Server'
    OTHER_SERVER = 'Other Server', 'Other Server'
    BACKUP_DEVICE = 'Backup device', 'Backup device'
    STORAGE_NAS = 'Storage - NAS', 'Storage - NAS'
    STORAGE_SAN = 'Storage - SAN', 'Storage - SAN'
    DATA_HISTORIAN = 'Data Historian', 'Data Historian'
    HMI = 'Human Machine Interface (HMI)', 'Human Machine Interface (HMI)'
    IDS_IPS_DETECTION = 'IDS/IPS Detection', 'IDS/IPS Detection'
    MTU = 'Master Terminal Unit (MTU)', 'Master Terminal Unit (MTU)'
    PLC = 'Programmable Logic Controller (PLC)', 'Programmable Logic Controller (PLC)'
    REMOTE_ACCESS = 'Remote Access', 'Remote Access'
    RTU = 'Remote Terminal Unit (RTU)', 'Remote Terminal Unit (RTU)'
    OTHER_HARDWARE = 'Other hardware', 'Other hardware'


class Status(models.TextChoices):
    IN_OPERATION = 'In operation', 'In operation'
    RETIRED = 'Retired', 'Retired'
    PENDING_SETUP = 'Pending Setup', 'Pending Setup'
    OFFLINE = 'Offline', 'Offline'
    NOT_DEFINED_YET = 'Not defined yet', 'Not defined yet'
    EXCEPTION = 'Exception', 'Exception'


class Device(models.Model):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 100

    MIN_SERIAL_NUMBER_LENGTH = 2
    MAX_SERIAL_NUMBER_LENGTH = 30

    MIN_OWNER_NAME_LENGTH = 2
    MAX_OWNER_NAME_LENGTH = 50

    MAX_STATUS_LENGTH = 20

    MAX_CATEGORY_LENGTH = 50

    MAX_SUBCATEGORY_LENGTH = 50

    MIN_MANUFACTURER_LENGTH = 1
    MAX_MANUFACTURER_LENGTH = 100

    MIN_MODEL_LENGTH = 1
    MAX_MODEL_LENGTH = 100

    MIN_DOMAIN_LENGTH = 1
    MAX_DOMAIN_LENGTH = 50

    device_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
        ),
        unique=True,
        null=False,
        blank=False,
    )

    domain = models.CharField(
        max_length=MAX_DOMAIN_LENGTH,
        validators=(
            MinLengthValidator(MIN_DOMAIN_LENGTH),
        ),
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=MAX_STATUS_LENGTH,
        choices=Status.choices,
        default=Status.NOT_DEFINED_YET,
    )

    category = models.CharField(
        max_length=MAX_CATEGORY_LENGTH,
        choices=Category.choices,
        default=Category.OTHER,
    )

    sub_category = models.CharField(
        max_length=MAX_SUBCATEGORY_LENGTH,
        choices=SubCategory.choices,
        default=SubCategory.OTHER_HARDWARE,
    )

    manufacturer = models.CharField(
        max_length=MAX_MANUFACTURER_LENGTH,
        validators=(
            MinLengthValidator(MIN_MANUFACTURER_LENGTH),
        ),
    )

    model = models.CharField(
        max_length=MAX_MODEL_LENGTH,
        validators=(
            MinLengthValidator(MIN_MODEL_LENGTH),
        ),
    )

    ip_address = models.GenericIPAddressField(
        unique=True,
        null=True,
        blank=True,
    )

    ip_address_sec = models.GenericIPAddressField(
        unique=True,
        null=True,
        blank=True,
    )

    serial_number = models.CharField(
        max_length=MAX_SERIAL_NUMBER_LENGTH,
        validators=(
            MinLengthValidator(MIN_SERIAL_NUMBER_LENGTH),
        ),
        unique=True,
        null=True,
        blank=True,
    )

    owner_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_OWNER_NAME_LENGTH),
        ),
        default='Unknown',
    )

    support = models.OneToOneField(
        to=Support,
        on_delete=models.CASCADE,
    )

    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.DO_NOTHING,
    )

    business = models.ForeignKey(
        to=Business,
        on_delete=models.DO_NOTHING,
    )
