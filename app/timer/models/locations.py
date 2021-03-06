from django.db import models
from .utils import InheritanceQuerySet
from .owners import Corporation

class LocationManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return InheritanceQuerySet(self.model)

    def select_subclasses(self, *subclasses):
        return self.get_query_set().select_subclasses(*subclasses)

    def get_subclass(self, *args, **kwargs):
        return self.get_query_set().select_subclasses().get(*args, **kwargs)

    def all_subclassed(self):
        return InheritanceQuerySet(model=self.model).select_subclasses()


class Location(models.Model):
    id = models.BigIntegerField('Location ID', primary_key=True)
    name = models.CharField('Location Name', max_length=200)
    x = models.BigIntegerField('X Location', null=True)
    y = models.BigIntegerField('Y Location', null=True)
    z = models.BigIntegerField('Z Location', null=True)

    objects = LocationManager()

    def __unicode__(self):
        return "%(name)s" % self.__dict__

    def get_subclass(self):
        return Location.objects.get_subclass(pk=self.pk)

    @property
    def get_type(self):
        return self.get_subclass().__class__.__name__

    class Meta:
        app_label = 'timer'


class Region(Location):

    @property
    def systems(self):
        return System.objects.filter(constellation__in=self.constellations.all())

    @property
    def planets(self):
        return Planet.objects.filter(system__constellation__in=self.constellations.all())

    @property
    def moons(self):
        return Moon.objects.filter(planet__system__constellation__in=self.constellations.all())

    class Meta:
        app_label = 'timer'


class Constellation(Location):
    region = models.ForeignKey(Region, related_name='constellations')

    @property
    def planets(self):
        return Planet.objects.filter(system__in=self.systems.all())

    @property
    def moons(self):
        return Moon.objects.filter(planet__system__in=self.systems.all())

    class Meta:
        app_label = 'timer'


class System(Location):
    constellation = models.ForeignKey(Constellation, related_name='systems')
    owner = models.ForeignKey(Corporation, related_name='systems', null=True)

    @property
    def moons(self):
        return Moon.objects.filter(planet__in=self.planets.all())

    class Meta:
        app_label = 'timer'


class Planet(Location):
    system = models.ForeignKey(System, related_name='planets')

    class Meta:
        app_label = 'timer'


class Moon(Location):
    planet = models.ForeignKey(Planet, related_name='moons')

    @property
    def system(self):
        return self.planet.system

    class Meta:
        app_label = 'timer'


class Station(Location):
    system = models.ForeignKey(System, related_name='stations')

    class Meta:
        app_label = 'timer'