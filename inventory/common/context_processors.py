from inventory.organization.models import Organization


def get_organization(request):
    try:
        organization = Organization.objects.first()
    except Organization.DoesNotExist:
        organization = None
    return {"organization": organization}
