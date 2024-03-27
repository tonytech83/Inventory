
from django.utils.timezone import now
from datetime import timedelta

from django.db.models import Case, When, Value, Count

from inventory.business.models import Business
from inventory.devices.models import Device, Category


def get_device_status_counts():
    status_counts = Device.objects.values('status').annotate(total=Count('status')).order_by('-total')

    labels = [status['status'] for status in status_counts]
    data = [status['total'] for status in status_counts]

    return labels, data


def get_devices_support_count():
    labels = ['No support', '3 months to 0', '6 to 3 months', '12 to 6 months', 'Good', 'Unknown']
    today = now().date()
    twelve_months_ago = today - timedelta(days=365)
    six_months_ago = today - timedelta(days=182)
    three_months_ago = today - timedelta(days=91)

    annotated_devices = Device.objects.annotate(
        support_status=Case(
            When(eos__lt=today, then=Value('No support')),
            When(eos__lte=today, eos__gt=three_months_ago, then=Value('3 months to 0')),
            When(eos__lte=six_months_ago, eos__gt=three_months_ago, then=Value('6 to 3 months')),
            When(eos__lte=twelve_months_ago, eos__gt=six_months_ago, then=Value('12 to 6 months')),
            When(eos__gt=twelve_months_ago, then=Value('Good')),
            default=Value('Unknown'),
        )
    )

    counts = annotated_devices.values('support_status').annotate(total=Count('id'))

    counts_dict = {label: 0 for label in labels}
    for count in counts:
        if count['support_status'] in counts_dict:
            counts_dict[count['support_status']] = count['total']

    counts_list = [counts_dict[label] for label in labels]

    return labels, counts_list


def get_business_by_categories():
    businesses = Business.objects.all()
    categories = [category[0] for category in Category.choices]

    data = {}

    for business in businesses:
        data[business.business_name] = []
        for category in categories:
            data[business.business_name].append(business.device_set.filter(category=category).count())

    return data, categories
