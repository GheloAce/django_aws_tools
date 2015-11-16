"""Signals from the django_bouncy app"""
# pylint: disable=invalid-name
from django.dispatch import Signal


# Any notification received
sns_notification = Signal(providing_args=["notification", "request"])
# New SubscriptionConfirmation received
sns_subscription = Signal(providing_args=["result", "notification"])
# New bounce or complaint received
sns_feedback = Signal(providing_args=["instance", "message", "notification"])
# Delivery
#sns_delivery = Signal(providing_args=["request",])