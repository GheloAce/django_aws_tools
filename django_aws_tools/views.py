import json, time, os, string, re, six
import logging
from datetime import datetime, timedelta, date
from copy import deepcopy
from decimal import Decimal
from time import mktime

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Python 2.7
    from urllib import urlopen

# django
from django import forms
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sessions.backends.db import Session
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models.loading import get_model
from django.http import (HttpResponseBadRequest , HttpResponseRedirect, 
                            QueryDict, HttpResponseForbidden, Http404)
from django.shortcuts import (HttpResponse, redirect, render_to_response, 
                                get_object_or_404, render)
from django.template import RequestContext, Context, Template
from django.template.defaultfilters import floatformat
from django.template.loader import render_to_string
from django.utils import timezone, translation
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic import (FormView, TemplateView, DetailView, 
                                    ListView, UpdateView)

# django_aws_tools
from .models import Bounce, Complaint, Delivery
from .utils import clean_time
from .signals import sns_notification, sns_subscription, sns_feedback

logger = logging.getLogger(__name__)

### SNS ###

VITAL_NOTIFICATION_FIELDS = [
    'Type', 'Message', 'Timestamp', 'Signature',
    'SignatureVersion', 'TopicArn', 'MessageId',
    'SigningCertURL'
]

VITAL_MESSAGE_FIELDS = [
    'notificationType', 'mail'
]

ALLOWED_TYPES = [
    'Notification', 'SubscriptionConfirmation', 'UnsubscribeConfirmation'
]


class SNSView(object):

    @staticmethod
    def process_message(message, data):
        """Function to process a JSON message delivered from Amazon"""  
        #if not set(VITAL_MESSAGE_FIELDS) <= set(message):
        #    return HttpResponse('Missing Vital Fields')

        if message.get('notificationType') == 'Complaint':
            return SNSView.process_complaint(message, data)

        if message.get('notificationType') == 'Bounce':
            return SNSView.process_bounce(message, data)

        if message.get('notificationType') == 'Delivery':
            return SNSView.process_delivery(message, data)

        # handle notifications
        else:
            return HttpResponse('Unknown notification type')


    @staticmethod
    def process_delivery(message, notification):
        """Function to process a delivery notification"""
        mail = message.get('mail')
        delivery = message.get('delivery')

        deliveries = []
        for recipient in delivery.get('recipients'):
            # Create each bounce record. Add to a list for reference later.
            deliveries += [Delivery.objects.create(
                sns_topic=notification.get('TopicArn'),
                sns_messageid=notification.get('MessageId'),
                mail_timestamp=clean_time(mail.get('timestamp')),
                mail_id=mail.get('messageId'),
                mail_from=mail.get('source'),
                address=recipient,
                reporting_mta=delivery.get('reportingMTA'),
                smtp_response=delivery.get('smtpResponse'),
            )]

        # Send signals for each bounce.
        for d in deliveries:
            sns_feedback.send(
                sender=Delivery,
                instance=d,
                message=message,
                notification=notification
            )

        return HttpResponse('Delivery Processed')

    @staticmethod
    def process_complaint(message, notification):
        """Function to process a complaint notification"""
        mail = message.get('mail')
        complaint = message.get('complaint')

        if 'arrivalDate' in complaint:
            arrival_date = clean_time(complaint.get('arrivalDate'))
        else:
            arrival_date = None

        complaints = []
        for recipient in complaint.get('complainedRecipients'):
            complaints += [Complaint.objects.create(
                sns_topic=notification.get('TopicArn'),
                sns_messageid=notification.get('MessageId'),
                mail_timestamp=clean_time(mail.get('timestamp')),
                mail_id=mail.get('messageId'),
                mail_from=mail.get('source'),
                address=recipient.get('emailAddress'),
                feedback_id=complaint.get('feedbackId'),
                feedback_timestamp=clean_time(complaint.get('timestamp')),
                useragent=complaint.get('userAgent'),
                feedback_type=complaint.get('complaintFeedbackType'),
                arrival_date=arrival_date
            )]

        for c in complaints:
            sns_feedback.send(
                    sender=Complaint,
                    instance=c,
                    message=message,
                    notification=notification
                )

        return HttpResponse('Complaint Processed')

    @staticmethod
    def process_bounce(message, notification):
        """Function to process a bounce notification"""
        mail = message.get('mail')
        bounce = message.get('bounce')

        bounces = []
        for recipient in bounce.get('bouncedRecipients'):
            # Create each bounce record. Add to a list for reference later.
            bounces += [Bounce.objects.create(
                sns_topic=notification.get('TopicArn'),
                sns_messageid=notification.get('MessageId'),
                mail_timestamp=clean_time(mail.get('timestamp')),
                mail_id=mail.get('messageId'),
                mail_from=mail.get('source'),
                address=recipient.get('emailAddress'),
                feedback_id=bounce.get('feedbackId'),
                feedback_timestamp=clean_time(bounce.get('timestamp')),
                hard=bool(bounce.get('bounceType') == 'Permanent'),
                bounce_type=bounce.get('bounceType'),
                bounce_subtype=bounce.get('bounceSubType'),
                reporting_mta=bounce.get('reportingMTA'),
                action=recipient.get('action'),
                status=recipient.get('status'),
                diagnostic_code=recipient.get('diagnosticCode')
            )]

        # Send signals for each bounce.
        for bounce in bounces:
            sns_feedback.send(
                sender=Bounce,
                instance=bounce,
                message=message,
                notification=notification
            )

        return HttpResponse('Bounce Processed')

    @staticmethod
    def approve_subscription(data):
        """
        Function to approve a SNS subscription with Amazon
        We don't do a ton of verification here, past making sure that the endpoint
        we're told to go to to verify the subscription is on the correct host
        """
        url = data.get('SubscribeURL')

        domain = urlparse(url).netloc
        pattern = getattr(
            settings,
            'SNS_SUBSCRIBE_DOMAIN_REGEX',
            r"sns.[a-z0-9\-]+.amazonaws.com$"
        )
        if not re.search(pattern, domain):
            #logger.error('Invalid Subscription Domain %s', url)
            return HttpResponseBadRequest('Improper Subscription Domain')

        try:
            result = urlopen(url).read()
            print result
            #logger.info('Subscription Request Sent %s', url)
        except urllib.HTTPError as error:
            result = error.read()
            #logger.warning('HTTP Error Creating Subscription %s', str(result))

        sns_subscription.send(
            sender='SNS Approve',
            result=result,
            notification=data
        )

        # Return a 200 Status Code
        return HttpResponse(six.u(result))


    class EndPoint(View):

        def post(self, request, *args, **kwargs):
            logger.info(request.body)

            if hasattr(settings, 'SNS_TOPIC_ARNS'):
                # get topic arn from request
                if 'HTTP_X_AMZ_SNS_TOPIC_ARN' not in request.META:
                    return HttpResponseBadRequest('No TopicArn Header')

                if (not request.META.get('HTTP_X_AMZ_SNS_TOPIC_ARN')
                        in settings.SNS_TOPIC_ARNS):
                    return HttpResponseBadRequest('Topic not found')

                # load JSON POST body
                try:
                    data = json.loads(request.body)
                except Exception, e:
                    print e
                    return HttpResponseBadRequest('Not Valid JSON')

                # check if all vital fields are available
                if not set(VITAL_NOTIFICATION_FIELDS) <= set(data):
                    msg = 'Request Missing Necessary Keys'
                    return HttpResponseBadRequest(msg)

                # ensure allowed notifications
                if not data.get('Type') in ALLOWED_TYPES:
                    msg = 'Unknown notification type'
                    return HttpResponseBadRequest(msg)

                # send signal to say verification has been received
                sns_notification.send(
                        sender='SNS EndPoint',
                        notification=data,
                        request=request,
                    )

                # subscription based messages
                if data.get('Type') == 'SubscriptionConfirmation':
                    # Allow the disabling of the auto-subscription feature
                    if not getattr(settings, 'SNS_AUTO_SUBSCRIBE', True):
                        raise Http404
                    # handle approved subscription
                    return SNSView.approve_subscription(data)
                elif data.get('Type') == 'UnsubscribeConfirmation':
                    # make own unsubscribe handler
                    return HttpResponse('UnsubscribeConfirmation Not Handled')

                # process message
                try:
                    message = json.loads(data.get('Message'))
                except ValueError:
                    return HttpResponse('Message is not valid JSON')

                return SNSView.process_message(message, data)

        @method_decorator(csrf_exempt)
        def dispatch(self, *args, **kwargs):
            return super(SNSView.EndPoint, self).dispatch(*args, **kwargs)