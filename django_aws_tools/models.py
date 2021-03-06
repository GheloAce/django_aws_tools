from django.db import models


# Models for the django_bouncy app
# Reference: http://docs.aws.amazon.com/ses/latest/DeveloperGuide/notification-examples.html


class Feedback(models.Model):
    """
    An abstract model for all SES Feedback Reports
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    sns_topic = models.CharField(max_length=350)
    sns_messageid = models.CharField(max_length=100)
    mail_timestamp = models.DateTimeField()
    mail_id = models.CharField(max_length=100)
    mail_from = models.EmailField()
    address = models.EmailField()
    feedback_id = models.CharField(max_length=100, null=True, blank=True)
    feedback_timestamp = models.DateTimeField(
        verbose_name="Feedback Time", null=True, blank=True)

    class Meta(object):
        abstract = True


class Bounce(Feedback):
    """
    A bounce report for an individual email address
    """
    hard = models.BooleanField(db_index=True, verbose_name="Hard Bounce")
    bounce_type = models.CharField(
        db_index=True, max_length=50, verbose_name="Bounce Type")
    bounce_subtype = models.CharField(
        db_index=True, max_length=50, verbose_name="Bounce Subtype")
    reporting_mta = models.TextField(blank=True, null=True)
    action = models.CharField(
        "Action", db_index=True, null=True, blank=True, max_length=150)
    status = models.CharField(
        db_index=True, null=True, blank=True, max_length=150)
    diagnostic_code = models.CharField(null=True, blank=True, max_length=150)

    class Meta(object):
        db_table = 'django_aws_tools_bounces'

    def __unicode__(self):
        return "%s %s Bounce (message from %s)" % (
            self.address, self.bounce_type, self.mail_from)


class Complaint(Feedback):
    """
    A complaint report for an individual email address
    """
    useragent = models.TextField(blank=True, null=True)
    feedback_type = models.CharField(
        db_index=True, blank=True, null=True, max_length=150,
        verbose_name="Complaint Type")
    arrival_date = models.DateTimeField(blank=True, null=True)

    class Meta(object):
        db_table = 'django_aws_tools_complaints'

    def __unicode__(self):
        return "%s Complaint (email sender: from %s)" % (
            self.address, self.mail_from)


class Delivery(Feedback):
    """
    Delivery
    """
    smtp_response = models.TextField(blank=True, null=True)
    reporting_mta = models.TextField(blank=True, null=True)

    class Meta(object):
        db_table = 'django_aws_tools_deliveries'
        verbose_name_plural = 'Deliveries'

    def __unicode__(self):
        return "Delivery (email message to: %s)" % (self.address,)
