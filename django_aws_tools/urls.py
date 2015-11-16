# DJANGO
from django.conf.urls import patterns, url
# LOCAL
from .views import SNSView


urlpatterns = patterns(
        '',
        url(r'^$', SNSView.EndPoint.as_view()),
    )