from django.conf.urls import patterns, url
from timer.views import TimerListView, TimerCreateView

urlpatterns = patterns('',
    url(r'^$', TimerListView.as_view(), name='timer-list'),
    url(r'^create/$', TimerCreateView.as_view(), name='timer-create')

)