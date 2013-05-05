from django.views.generic import ListView
from django.utils.timezone import now
from timer.models import Timer


class TimerListView(ListView):
    model = Timer

    def get_queryset(self):
        qs = super(TimerListView, self).get_queryset()
        if 'active' in self.kwargs:
            qs = qs.filter(expiry_datetime__gt=now())
        return qs

