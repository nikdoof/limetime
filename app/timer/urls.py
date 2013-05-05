from django.conf.urls import patterns, url
from timer.views import TimerListView

urlpatterns = patterns('',
    url(r'^$', TimerListView.as_view(), name='timer-list'),
)