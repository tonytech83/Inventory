from datetime import timedelta

from django import template
from django.db.models import Q, QuerySet
from django.utils.timezone import now

register = template.Library()


@register.simple_tag
def count_no_support_devices(business):
    if isinstance(business, QuerySet):
        return sum([b.device_set.filter(eos__lt=now().date()).count() for b in business])

    return business.device_set.filter(eos__lt=now().date()).count()


@register.simple_tag
def count_devices_in_support(business):
    today = now().date()
    one_year_from_now = today + timedelta(days=365)

    if isinstance(business, QuerySet):
        return sum([b.device_set.filter(eos__gt=one_year_from_now).count() for b in business])

    return business.device_set.filter(eos__gt=one_year_from_now).count()


@register.simple_tag
def count_devices_unknown_support(business):
    if isinstance(business, QuerySet):
        return sum([b.device_set.filter(eos=None).count() for b in business])

    return business.device_set.filter(eos=None).count()


@register.simple_tag
def count_lt_year_gt_six_month(business):
    today = now().date()
    six_months_from_now = today + timedelta(days=182)
    one_year_from_now = today + timedelta(days=365)

    query = Q(eos__gt=six_months_from_now) & Q(eos__lt=one_year_from_now)

    if isinstance(business, QuerySet):
        return sum([b.device_set.filter(query).count() for b in business])

    return business.device_set.filter(query).count()


@register.simple_tag
def count_lt_six_gt_three_months(business):
    today = now().date()
    six_months_from_now = today + timedelta(days=182)
    three_months_from_now = today + timedelta(days=90)

    query = Q(eos__gt=three_months_from_now) & Q(eos__lt=six_months_from_now)

    if isinstance(business, QuerySet):
        return sum([b.device_set.filter(query).count() for b in business])

    return business.device_set.filter(query).count()


@register.simple_tag
def count_lt_three_months_and_no_support(business):
    today = now().date()
    three_months_from_now = today + timedelta(days=90)

    query = Q(eos__gt=today) & Q(eos__lt=three_months_from_now)

    if isinstance(business, QuerySet):
        return sum([b.device_set.filter(query).count() for b in business])

    return business.device_set.filter(query).count()


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
    if isinstance(business, QuerySet):
        return sum([b.device_set.filter(status__icontains=status).count() for b in business])

    return business.device_set.filter(status=status).count()


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
