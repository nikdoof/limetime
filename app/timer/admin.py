from django.contrib import admin
from timer.models import Timer


class TimerAdmin(admin.ModelAdmin):
    readonly_fields = ['location']

admin.site.register(Timer, admin.ModelAdmin)