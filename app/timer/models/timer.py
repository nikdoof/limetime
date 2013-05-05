from django.db import models
from django.utils.timezone import now


class Timer(models.Model):

    STATE_ACTIVE = 1
    STATE_EXPIRED = 2

    STATE_CHOICES = (
        (STATE_ACTIVE, 'Active'),
        (STATE_EXPIRED, 'Expired'),
    )

    TYPE_SHEILD_REENFORCEMENT = 1
    TYPE_ARMOR_REENFORCEMENT = 2

    TYPE_CHOICES = (
        (TYPE_SHEILD_REENFORCEMENT, 'Sheild Reenforcement'),
        (TYPE_ARMOR_REENFORCEMENT, 'Armor Reenforcement'),
    )

    location = models.ForeignKey('timer.Location', related_name='timers')
    expiration = models.DateTimeField('Timer Expiration')
    reenforcement_type = models.PositiveIntegerField('Timer Type', choices=TYPE_CHOICES)

    @property
    def state(self):
        if self.expiration <= now():
            return self.STATE_EXPIRED
        return self.STATE_ACTIVE

    class Meta:
        app_label = 'timer'
        ordering = ['-expiration']