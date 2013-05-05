from django.core.management.base import BaseCommand
from django.db import transaction
from timer.models import Station, System
from eveapi import EVEAPIConnection

class Command(BaseCommand):
    args = ''
    help = 'Updates conquerable stations from the EVE API'

    def handle(self, *args, **options):
        api = EVEAPIConnection()

        station_list = api.eve.ConquerableStationList().outposts
        print 'Updating %d stations... ' % len(station_list)
        with transaction.commit_on_success():
            for station in station_list:
                try:
                    obj = Station.objects.get(pk=station.stationID)
                except Station.DoesNotExist:
                    obj = Station(pk=station.stationID)
                    obj.system, created = System.objects.get_or_create(pk=station.solarSystemID)
                obj.name = station.stationName
                obj.save()
        print 'Done'