from django.conf.urls import patterns, url

# django_aws_tools
from .views import SNSView

urlpatterns = patterns(
        '',
        url(r'^$', SNSView.EndPoint.as_view()),
    )