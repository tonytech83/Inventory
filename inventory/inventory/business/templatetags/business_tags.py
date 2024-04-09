from datetime import timedelta

from django import template
from django.db.models import Q, QuerySet
from django.utils.timezone import now

register = template.Library()


# Support
def count_devices_by_filter(business, filter_query=None):
    if isinstance(business, QuerySet):
        return sum(
            [b.device_set.filter(filter_query).count() if filter_query else b.device_set.count()
             for b in business]
        )

    return business.device_set.filter(filter_query).count() if filter_query else business.device_set.count()


@register.simple_tag
def count_no_support_devices(business):
    filter_query = Q(eos__lt=now().date())
    return count_devices_by_filter(business, filter_query)


@register.simple_tag
def count_devices_in_support(business):
    today = now().date()
    one_year_from_now = today + timedelta(days=365)
    filter_query = Q(eos__gt=one_year_from_now)
    return count_devices_by_filter(business, filter_query)


@register.simple_tag
def count_devices_unknown_support(business):
    filter_query = Q(eos=None)
    return count_devices_by_filter(business, filter_query)


@register.simple_tag
def count_lt_year_gt_six_month(business):
    today = now().date()
    six_months_from_now = today + timedelta(days=182)
    one_year_from_now = today + timedelta(days=365)
    filter_query = Q(eos__gte=six_months_from_now) & Q(eos__lt=one_year_from_now)
    return count_devices_by_filter(business, filter_query)


@register.simple_tag
def count_lt_six_gt_three_months(business):
    today = now().date()
    six_months_from_now = today + timedelta(days=182)
    three_months_from_now = today + timedelta(days=90)
    filter_query = Q(eos__gte=three_months_from_now) & Q(eos__lt=six_months_from_now)
    return count_devices_by_filter(business, filter_query)


@register.simple_tag
def count_lt_three_months_and_no_support(business):
    today = now().date()
    three_months_from_now = today + timedelta(days=90)
    filter_query = Q(eos__gte=today) & Q(eos__lt=three_months_from_now)
    return count_devices_by_filter(business, filter_query)


# Not reviewed devices
@register.simple_tag
def count_no_reviewed_devices(business):
    devices = business.device_set.all()

    return sum(not device.is_reviewed for device in devices)


# Status
@register.filter(name='get_query_param')
def get_query_param(value, arg):
    """Fetch a query parameter value by its name."""
    return value.get(arg, '')


@register.simple_tag
def count_by_status(business, status):
    if isinstance(business, QuerySet):
        return sum([b.device_set.filter(status__icontains=status).count() for b in business])

    return business.device_set.filter(status=status).count()


# Category
@register.simple_tag
def count_by_category(business, category):
    if isinstance(business, QuerySet):
        return sum([b.device_set.filter(category__icontains=category).count() for b in business])

    return business.device_set.filter(category=category).count()


# Risk

@register.simple_tag
def risk_below_five(business):
    devices = business.device_set.all()

    filtered_devices = [device for device in devices if device.risk_score < 5]

    return len(filtered_devices)


@register.simple_tag
def between_five_and_ten(business):
    devices = business.device_set.all()

    filtered_devices = [device for device in devices if 5 <= device.risk_score <= 10]

    return len(filtered_devices)


@register.simple_tag
def above_ten(business):
    devices = business.device_set.all()

    filtered_devices = [device for device in devices if device.risk_score > 10]

    return len(filtered_devices)
