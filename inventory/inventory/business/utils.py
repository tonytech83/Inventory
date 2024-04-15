from datetime import timedelta
from django.utils.timezone import now
from django.db.models import ExpressionWrapper, F, fields


def prepare_device_list(device_queryset):
    """
    Converts a queryset of device objects into a list of dictionaries containing detailed device information.

    Each device in the queryset is transformed into a dictionary with key attributes such as device ID, name, domain,
    etc. Supplier-related information is also included.

    Args:
        device_queryset (QuerySet): A Django QuerySet containing device objects that need to be processed.

    Returns:
        list of dict: A list where each element is a dictionary representing a device with all its attributes and
        associated data extracted and formatted as described.
    """

    device_list = []

    for device in device_queryset:
        device_dict = {
            'id': device.id,
            'device_name': device.device_name,
            'domain': device.domain,
            'description': device.description,
            'status': device.status,
            'manufacturer': device.manufacturer,
            'model': device.model,
            'ip_address': device.ip_address,
            'ip_address_sec': device.ip_address_sec,
            'operating_system': device.operating_system,
            'building': device.building,
            'category': device.category,
            'sub_category': device.sub_category,
            'serial_number': device.serial_number,
            'owner_name': device.owner_name,
            # Support fields
            'support_model': device.support_model,
            'purchase_order_number': device.purchase_order_number,
            'invoice_img': device.invoice_img.url if device.invoice_img else None,
            'sos': device.sos.isoformat() if device.sos else None,
            'eos': device.eos.isoformat() if device.eos else None,
            'eol': device.eol.isoformat() if device.eol else None,
            # Risk fields
            'business_processes_at_risk': device.business_processes_at_risk,
            'impact': device.impact,
            'likelihood': device.likelihood,
            # Supplier
            'supplier_name': device.supplier_display,
        }
        device_list.append(device_dict)

    return device_list


def filter_devices_queryset(self, business):
    """
    Filters a queryset of devices associated with a given business based on various criteria received via request parameters.

    The function applies multiple filters on device status, review dates, support periods, and risk scores based on
    criteria specified in the request's GET parameters. It includes date ranges for filtering devices needing review
    or nearing the end of support, and calculates risk scores to filter by predefined risk thresholds.

    Args:
        business (Business): The business instance from which device data is to be filtered.

    Returns:
        QuerySet: A Django QuerySet containing devices that match the filtering criteria specified in the request.

    Filtering includes:
    - Device status such as 'In operation', 'Decommissioned', etc.
    - Devices not reviewed in the last year.
    - Devices with support ending within different future timeframes.
    - Devices categorized by risk scores below 5, between 5 and 10, and above 10.
    """

    device_queryset = business.device_set.all()
    filters = self.request.GET

    # Periods
    today = now().date()
    one_year_ago = now() - timedelta(days=365)
    six_months_ahead = now() + timedelta(days=182)
    one_year_ahead = now() + timedelta(days=365)
    one_year_from_now = today + timedelta(days=365)
    six_months_from_now = today + timedelta(days=182)
    three_months_from_now = today + timedelta(days=90)

    # Filters based on device status
    if 'in_operation' in filters:
        device_queryset = device_queryset.filter(status='In operation')
    if 'is_decommissioned' in filters:
        device_queryset = device_queryset.filter(status='Decommissioned')
    if 'is_pending_setup' in filters:
        device_queryset = device_queryset.filter(status='Pending Setup')
    if 'is_offline' in filters:
        device_queryset = device_queryset.filter(status='Offline')
    if 'not_defined' in filters:
        device_queryset = device_queryset.filter(status='Not defined yet')
    if 'is_exception' in filters:
        device_queryset = device_queryset.filter(status='Exception')

    # Filters based on device review and support periods
    if 'no_reviewed' in filters:
        device_queryset = device_queryset.filter(updated_at__lte=one_year_ago)

    if 'no_support' in filters:
        device_queryset = device_queryset.filter(eos__lt=now().date())

    if 'lt_three_months_and_no_support' in filters:
        device_queryset = device_queryset.filter(eos__range=(today, three_months_from_now))

    if 'lt_six_gt_three_months' in filters:
        device_queryset = device_queryset.filter(eos__range=(three_months_from_now, six_months_from_now))

    if 'lt_year_gt_six_month' in filters:
        device_queryset = device_queryset.filter(eos__range=(six_months_ahead, one_year_ahead))

    if 'count_devices_in_support' in filters:
        device_queryset = device_queryset.filter(eos__gt=one_year_from_now)

    if 'count_devices_unknown_support' in filters:
        device_queryset = device_queryset.filter(eos=None)

    # Filters based on risk
    if 'risk_below_five' in filters:
        device_queryset = device_queryset.annotate(
            calculated_risk_score=ExpressionWrapper(
                F('impact') * F('likelihood'),
                output_field=fields.FloatField()
            )
        ).filter(calculated_risk_score__lt=5)

    if 'between_five_and_ten' in filters:
        device_queryset = device_queryset.annotate(
            calculated_risk_score=ExpressionWrapper(
                F('impact') * F('likelihood'),
                output_field=fields.FloatField()
            )
        ).filter(calculated_risk_score__gte=5, calculated_risk_score__lte=10)

    if 'above_ten' in filters:
        device_queryset = device_queryset.annotate(
            calculated_risk_score=ExpressionWrapper(
                F('impact') * F('likelihood'),
                output_field=fields.FloatField()
            )
        ).filter(calculated_risk_score__gt=10)

    return device_queryset


def prepare_suppliers_list(suppliers):
    """
    Prepare list of dictionaries with suppliers.
    """

    return [{
        "id": supplier.id,
        "name": supplier.name,
        "contact_name": supplier.contact_name,
        "phone_number": supplier.phone_number,
        "email": supplier.email,
    } for supplier in suppliers]
