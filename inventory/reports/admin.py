from django.contrib import admin

from inventory.reports.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("report_owner", "turn_on", "day_of_week")

    def report_owner(self, obj):
        return obj.profile.account.email

    report_owner.short_description = "Report Owner"
