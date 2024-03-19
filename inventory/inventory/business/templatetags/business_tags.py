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


@register.filter(name='get_query_param')
def get_query_param(value, arg):
    """Fetch a query parameter value by its name."""
    return value.get(arg, '')


@register.simple_tag
def count_by_status(business, status):
    return business.device_set.filter(status=status).count()
