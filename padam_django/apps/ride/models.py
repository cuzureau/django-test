from django.db import models
from typing import Optional
from datetime import datetime


class BusStop(models.Model):
    name = models.CharField(max_length=100)
    place = models.ForeignKey('geography.Place', on_delete=models.CASCADE)
    passage_datetime = models.DateTimeField(default=None, null=True)

    def __str__(self) -> str:
        return f'Bus Stop: {self.place.name} - {self.passage_datetime.strftime("%m/%d/%Y %H:%M")} (id: {self.pk})'
    

class BusShift(models.Model):
    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE, null=False, blank=False)
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE, null=False, blank=False)
    stops = models.ManyToManyField('BusStop', blank=True)

    @property
    def departure_datetime(self) -> Optional[datetime]:
        if self.stops.exists():
            return self.stops.all().order_by('passage_datetime').first().passage_datetime
        else:
            return None

    @property
    def arrival_datetime(self) -> Optional[datetime]:
        if self.stops.exists():
            return self.stops.all().order_by('-passage_datetime').first().passage_datetime
        else:
            return None

    @property
    def total_duration(self) -> Optional[datetime]:
        if self.stops.exists():
            return self.arrival_datetime - self.departure_datetime
        else:
            return None

    def __str__(self) -> str:
        return f"Bus Shift: Bus:{self.bus.licence_plate}, Driver: {self.driver.user.username} (id: {self.pk})"
