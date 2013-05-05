from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.api import Api
from timer.models import Location


class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        resource_name = 'location'
        include_resource_uri = False
        limit = 100
        excludes = ['x', 'y', 'z']
        filtering = {
            'name': ['exact', 'contains'],
        }

v1_api = Api(api_name='1.0')
v1_api.register(LocationResource())
