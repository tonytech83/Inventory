from celery import shared_task
from django.contrib.auth import get_user_model, user_logged_in
from django.core.mail import EmailMessage

from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from inventory import settings
from inventory.accounts.models import Profile
from inventory.accounts.utils import send_the_email

UserModel = get_user_model()


@receiver(pre_save, sender=UserModel)
def set_first_user_superuser(sender, instance, **kwargs):
    # Use a transaction.atomic block to ensure thread safety
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

    # send_successful_registration_email(instance)
    send_successful_registration_email_task.delay(instance.pk)
    Profile.objects.create(account=instance)


@shared_task
def send_successful_registration_email_task(user_id):

    user = UserModel.objects.get(pk=user_id)

    context = {
        'user': user,
    }
    subject = 'Registration greetings!'
    message = render_to_string('emails/email_greeting.html', context)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list
    )
    email.content_subtype = 'html'
    email.send()


# def send_successful_registration_email(user):
#     context = {
#         'user': user,
#     }
#     return send_the_email(
#         subject='Registration greetings!',
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=(user.email,),
#         template_name='emails/email_greeting.html',
#         context=context,
#     )


@receiver(user_logged_in)
def set_first_login(sender, request, user, **kwargs):
    # Check if this is the first login
    if user.last_login is None:
        request.session['first_login'] = True
