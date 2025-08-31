from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from inventory import settings
from inventory.accounts.models import Profile
from inventory.reports.models import Report

UserModel = get_user_model()


@receiver(pre_save, sender=UserModel)
def set_first_user_superuser(sender, instance, **kwargs):
    with transaction.atomic():
        if not UserModel.objects.exists():
            instance.is_staff = True
            instance.is_superuser = True
        else:
            # Ensure users after first are only staff
            if not instance.pk:
                instance.is_staff = True
                instance.is_superuser = False


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    profile = Profile.objects.create(account=instance)
    send_successful_registration_email_task.delay(instance.pk)
    Report.objects.create(profile=profile)


@shared_task
def send_successful_registration_email_task(user_id):
    user = UserModel.objects.get(pk=user_id)

    context = {
        "user": user,
    }
    subject = "Registration greetings!"
    message = render_to_string("emails/email_greeting.html", context)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    email = EmailMessage(
        subject=subject, body=message, from_email=from_email, to=recipient_list
    )
    email.content_subtype = "html"
    email.send()
