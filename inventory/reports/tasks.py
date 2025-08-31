from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from inventory import settings

from .models import Report

logger = get_task_logger(__name__)

UserModel = get_user_model()


@shared_task(bind=True, max_retries=3, default_retry_delay=60 * 5)
def send_report_email(self, user_id):
    """
    Celery task to send a weekly report email to a specified user based on their user_id.

    This task retrieves a user's report settings from the Report model. If reporting is enabled (turn_on=True),
    it generates and sends an email containing a custom report. The task is configured to retry up to three times
    if an exception occurs during execution, with a delay of five minutes between retries.

    Parameters
    ----------
        user_id (int): The unique identifier for the user for whom the report is to be sent.

    Raises
    ------
        Report.DoesNotExist: If no Report object exists for the given user_id.
        Exception: General exception for catching other unforeseen errors during the email sending process, which
                   triggers a retry of the task.

    """
    try:
        report = Report.objects.get(profile__account_id=user_id)

        if report.turn_on:
            subject = "Weekly Report"
            message = generate_report_content(user_id)
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [report.profile.account.email]

            print(recipient_list)

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list,
            )
            email.content_subtype = "html"
            email.send()

    except Report.DoesNotExist:
        logger.error("This user has not set report.")
    except Exception as exception:
        logger.error("Problem sending report.")
        raise self.retry(exc=exception)


def generate_report_content(user_id):
    """Generates the HTML content for a report email by rendering a Django template with user-specific data."""
    user = UserModel.objects.get(pk=user_id)

    context = {
        "user": user,
        "businesses": user.owner.all(),
    }

    message = render_to_string("emails/report.html", context)

    return message


@shared_task
def check_and_send_reports():
    """Celery task to check for and initiate the sending of scheduled reports based on the current day of the week."""
    day_of_week = timezone.now().strftime("%A")
    reports_to_send = Report.objects.filter(day_of_week=day_of_week, turn_on=True)

    for report in reports_to_send:
        send_report_email.delay(report.profile.account.id)
