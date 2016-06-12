from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Entity(models.Model):
    # Constants
    INSTITUTIONAL   = 'IN' # Institutionnel (Météo-France, CIRAD)
    ORGANIZATION    = 'OR' # Association (MétéoR OI)
    COMPANY         = 'CO' # Société
    PRIVATE         = 'PR' # Station personnelle

    ENTITY_CHOICES = (
        (INSTITUTIONAL  , 'Institutionnel'),
        (ORGANIZATION   , 'Association'),
        (COMPANY        , 'Société'),
        (PRIVATE        , 'Privé'),
    )

    user        = models.ForeignKey(User)

    name        = models.CharField(max_length=200)
    description = models.TextField()
    entity_type = models.CharField(max_length=2,
                                   choices=ENTITY_CHOICES)
    email       = models.EmailField()
    phone       = models.CharField(max_length=16)
    address     = models.TextField()

    def __str__(self):
        return self.name    

class Network(models.Model):
    owner       = models.ForeignKey(Entity)

    name        = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Site(models.Model):
    owner         = models.ForeignKey(Entity)

    code          = models.CharField(max_length=10, unique=True)
    description   = models.TextField()
    address       = models.TextField()
    postal_code   = models.PositiveIntegerField()
    town          = models.CharField(max_length=30)
    gps_latitude  = models.DecimalField(max_digits=10, decimal_places=7)
    gps_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    altitude      = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.code

class Brand(models.Model):
    name    = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class InstrumentModel(models.Model):
    # Constants
    MANUEL  = 'MAN'
    AUTO    = 'AUT'

    READING_TYPE_CHOICES = (
        (MANUEL , 'Instrument manuel'),
        (AUTO   , 'Instrument automatique'),
    )

    # Constants
    ANEMOMETER   = 'ANM' # Anémomètre
    RAIN_GAUGE   = 'PLG' # Pluviographe (auto) / Pluviomètre (manuel)
    THERMOMETER  = 'THM' # Thermomètre
    HYGROMETER   = 'HYM' # Hygromètre
    THERMO_HYGRO = 'THH' # Thermomètre & Hygromètre
    PYRANOMETER  = 'PYM' # Pyranomètre
    UV_SENSOR    = 'UVS' # Capteur UV

    TYPE_CHOICES = (
        (ANEMOMETER  , 'Anémomètre'),
        (RAIN_GAUGE  , 'Pluviographe / Pluviomètre'),
        (THERMOMETER , 'Thermomètre'),
        (HYGROMETER  , 'Hygromètre'),
        (THERMO_HYGRO, 'Thermomètre & Hygromètre'),
        (PYRANOMETER , 'Pyranomètre'),
        (UV_SENSOR   , 'Capteur UV'),
    )

    brand        = models.ForeignKey(Brand)

    name         = models.CharField(max_length=30)
    reading_type = models.CharField(max_length=3,
                                    choices=READING_TYPE_CHOICES)
    sensor_type  = models.CharField(max_length=3,
                                    choices=TYPE_CHOICES)
    precision    = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s' % (self.brand, self.name)

class StationModel(models.Model):
    # Constants
    DIRECT_READING   = 'RE' # Lecture directe
    TAPE_RECORDER    = 'TP' # Enregistreur à bande (station auto)
    DIGITAL_RECORDER = 'DR' # Enregistreur numérique (station auto)
    OTHER            = 'OT' # Autre type de station

    TYPE_CHOICES = (
        (DIRECT_READING  , 'Lecture directe'),
        (TAPE_RECORDER   , 'Station auto (Enregistreurs à bande)'),
        (DIGITAL_RECORDER, 'Station auto (Enregistreurs numériques)'),
        (OTHER           , 'Autre type de station'),
    )

    brand        = models.ForeignKey(Brand)
    instruments  = models.ManyToManyField(InstrumentModel)

    name         = models.CharField(max_length=40)
    description  = models.TextField()
    station_type = models.CharField(max_length=2,
                                    choices=TYPE_CHOICES)

    def __str__(self):
        return '%s %s (%s)' % (self.brand,
                               self.name,
                               self.get_station_type_display())

class Station(models.Model):
    network       = models.ForeignKey(Network)
    owner         = models.ForeignKey(Entity)
    site          = models.ForeignKey(Site)
    station_model = models.ForeignKey(StationModel)

    name          = models.CharField(max_length=100)
    date_start    = models.DateTimeField()
    date_end      = models.DateTimeField()
    description   = models.TextField()
    auto_transmit = models.BooleanField()

    def __str__(self):
        return '[%s - %s] %s (%s)' (self.network, self.site.code, self.name,
                                    self.station_model)

class Sensor(models.Model):
    station     = models.ForeignKey(Station)
    sensor_model = models.ForeignKey(InstrumentModel)

    description  = models.TextField()
    date_start   = models.DateTimeField()
    date_end     = models.DateTimeField()

    def __str__(self):
        return '[%s - %s] %s (%s)' (self.station.network,
                                    self.station.site.code,
                                    self.name,
                                    self.station.name)

    def is_active(self):
        return self.date_end > timezone.now()


class Archive(models.Model):
    # Constants
    UNIT_METRIC  = 'ME'
    UNIT_US      = 'US'

    UNIT_TYPE_CHOICES = (
        (UNIT_METRIC, 'Unités métriques'),
        (UNIT_US    , 'Unités US'),
    )
    station  = models.ForeignKey(Station)
    site     = models.ForeignKey(Site)

    date     = models.DateTimeField()
    interval = models.DurationField()
    units    = models.CharField(max_length=2,
                                choices=UNIT_TYPE_CHOICES)
   
    temperature      = models.DecimalField(max_digits=4, decimal_places=2)
    temperature2     = models.DecimalField(max_digits=4, decimal_places=2)
    humidity         = models.PositiveSmallIntegerField()
    dewpoint         = models.DecimalField(max_digits=4, decimal_places=2)
    windchill        = models.DecimalField(max_digits=4, decimal_places=2)
    heatindex        = models.DecimalField(max_digits=4, decimal_places=2)
    pressure         = models.DecimalField(max_digits=5, decimal_places=1)
    wind_direction   = models.DecimalField(max_digits=4, decimal_places=1)
    wind             = models.DecimalField(max_digits=5, decimal_places=2)
    wind_gust        = models.DecimalField(max_digits=5, decimal_places=2)
    wind_gust_dir    = models.DecimalField(max_digits=5, decimal_places=2)
    wind_2min        = models.DecimalField(max_digits=5, decimal_places=2)
    wind_10min       = models.DecimalField(max_digits=5, decimal_places=2)
    rain             = models.DecimalField(max_digits=5, decimal_places=2)
    rain_rate        = models.DecimalField(max_digits=6, decimal_places=2)
    uv_radiation     = models.DecimalField(max_digits=3, decimal_places=1)
    solar_radiation  = models.PositiveSmallIntegerField()
    et               = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '[%s] %s' % (self.site.code, self.date)
