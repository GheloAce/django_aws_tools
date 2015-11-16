# PYTHON
import csv
# DJANGO
from django.contrib import admin
from django.shortcuts import HttpResponse
from django.utils.encoding import smart_str
# LOCAL
# django_aws_tools
from .models import Bounce, Complaint, Delivery


@admin.register(Bounce)
class BounceAdmin(admin.ModelAdmin):
    actions = ('bounce_csv',)
    search_fields = ('address',)

    # noinspection PyMethodMayBeStatic
    def bounce_csv(self, request, queryset):
        # PREPARE
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=bounces.csv'
        writer = csv.writer(response, csv.excel)
        # PROCESS
        response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"ID"),
            smart_str(u"MESSAGE ID"),
            smart_str(u"TIMESTAMP"),
            smart_str(u"MAIL FROM"),
            smart_str(u"MAIL TO"),
            smart_str(u"BOUNCE TYPE"),
            smart_str(u"BOUNCE SUBTYPE"),
            smart_str(u"REPORTING MTA"),
            smart_str(u"ACTION"),
            smart_str(u"STATUS"),
            smart_str(u"DIAGNOSTIC CODE")])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk or ''),
                smart_str(obj.sns_messageid or ''),
                smart_str(obj.mail_timestamp or ''),
                smart_str(obj.mail_from or ''),
                smart_str(obj.address or ''),
                smart_str(obj.bounce_type or ''),
                smart_str(obj.bounce_subtype or ''),
                smart_str(obj.reporting_mta or ''),
                smart_str(obj.action or ''),
                smart_str(obj.status or ''),
                smart_str(obj.diagnostic_code or '')])
        # CONCLUDE
        return response

    bounce_csv.short_description = u"Export CSV"


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    actions = ('complaint_csv',)

    # noinspection PyMethodMayBeStatic
    def complaint_csv(self, request, queryset):
        # PREPARE
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=complaints.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
        # PROCESS
        writer.writerow([
            smart_str(u"ID"),
            smart_str(u"MESSAGE ID"),
            smart_str(u"TIMESTAMP"),
            smart_str(u"MAIL FROM"),
            smart_str(u"MAIL TO"),
            smart_str(u"USERAGENT"),
            smart_str(u"COMPLAINT TYPE"),
            smart_str(u"ARRIVAL DATE")])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk or ''),
                smart_str(obj.sns_messageid or ''),
                smart_str(obj.mail_timestamp or ''),
                smart_str(obj.mail_from or ''),
                smart_str(obj.address or ''),
                smart_str(obj.useragent or ''),
                smart_str(obj.feedback_type or ''),
                smart_str(obj.arrival_date or '')])
        # CONCLUDE
        return response

    complaint_csv.short_description = u"Export CSV"


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    actions = ('delivery_csv',)

    # noinspection PyMethodMayBeStatic
    def delivery_csv(self, request, queryset):
        # PREPARE
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=deliveries.csv'
        writer = csv.writer(response, csv.excel)
        # PROCESS
        response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"ID"),
            smart_str(u"MESSAGE ID"),
            smart_str(u"TIMESTAMP"),
            smart_str(u"MAIL FROM"),
            smart_str(u"MAIL TO"),
            smart_str(u"SMTP RESPONSE"),
            smart_str(u"REPORTIN MTA")])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk or ''),
                smart_str(obj.sns_messageid or ''),
                smart_str(obj.mail_timestamp or ''),
                smart_str(obj.mail_from or ''),
                smart_str(obj.address or ''),
                smart_str(obj.smtp_response or ''),
                smart_str(obj.reporting_mta or '')])
        # CONCLUDE
        return response

    delivery_csv.short_description = u"Delivery CSV"