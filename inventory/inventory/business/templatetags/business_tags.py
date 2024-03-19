from django import template
from django.utils.timezone import now

register = template.Library()


@register.simple_tag
def count_no_support_devices(business):
    return business.device_set.filter(support__eos__lt=now().date()).count()


@register.simple_tag
def count_no_reviewed_devices(business):
    devices = business.device_set.all()

    return sum(not device.is_reviewed for device in devices)


@register.simple_tag
def count_in_operation_devices(business):
    return business.device_set.filter(status='In operation').count()


@register.simple_tag
def count_is_decommissioned_devices(business):
    return business.device_set.filter(status='Decommissioned').count()
