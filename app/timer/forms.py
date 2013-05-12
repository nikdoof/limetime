from django import forms
from timer.models import Timer, Location


class TimerForm(forms.ModelForm):

    location = forms.ModelChoiceField(Location.objects.none())

    class Meta:
        model = Timer