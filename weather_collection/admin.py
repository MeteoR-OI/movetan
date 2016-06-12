from django.contrib import admin

# Register your models here.
from .models import Entity, Network, Site, Brand, InstrumentModel, \
                    StationModel, Station, Sensor, Archive


admin.site.register(Entity)
admin.site.register(Network)
admin.site.register(Site)
admin.site.register(Brand)
admin.site.register(InstrumentModel)
admin.site.register(StationModel)
admin.site.register(Station)
admin.site.register(Sensor)
admin.site.register(Archive)
