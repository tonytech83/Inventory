from django.db.models import Count

from inventory.devices.models import Device


def get_device_status_counts():
    status_counts = Device.objects.values('status').annotate(total=Count('status')).order_by('-total')

    labels = [status['status'] for status in status_counts]
    data = [status['total'] for status in status_counts]

    print(labels)

    return labels, data
