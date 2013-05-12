from django.views.generic import ListView, CreateView
from django.utils.timezone import now
from timer.models import Timer, Location, Station, Moon, System
from timer.forms import TimerForm


class TimerCreateView(CreateView):
    model = Timer
    form_class = TimerForm


class TimerListView(ListView):
    model = Timer
    template_name = 'timer/timer_list.html'

    def get_queryset(self):
        qs = super(TimerListView, self).get_queryset().select_related('location', 'station', 'moon', 'system')

        if int(self.request.GET.get('all', 0)) == 0:
            qs = qs.filter(expiration__gt=now())

        type = int(self.request.GET.get('type', 0))
        if type == 1:
            qs = [m for m in qs if m.location.get_type == 'Station']
        if type == 2:
            qs = [m for m in qs if m.location.get_type == 'System']
        if type == 3:
            qs = [m for m in qs if m.location.get_type == 'Moon']
        return qs


    def get_context_data(self, **kwargs):
        ctx = super(TimerListView, self).get_context_data(**kwargs)
        ctx.update({
            'list_all': int(self.request.GET.get('all', 0)),
            'list_type': int(self.request.GET.get('type', 0)),
        })
        return ctx