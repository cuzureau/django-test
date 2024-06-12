from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q, QuerySet

from ..fleet.models import Bus, Driver
from .models import BusShift


class BusShiftForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = ['bus', 'driver', 'stops']

    def clean(self) -> None:
        cleaned_data = super().clean()
        bus = cleaned_data.get('bus')
        stops = cleaned_data.get('stops')
        driver = cleaned_data.get('driver')

        self.validate_minimum_stops(stops)

        departure_datetime = stops.order_by('passage_datetime').first().passage_datetime
        arrival_datetime = stops.order_by('-passage_datetime').first().passage_datetime

        self.check_bus_overlaps(departure_datetime, arrival_datetime, bus)
        self.check_driver_overlaps(departure_datetime, arrival_datetime, driver)
            

    def validate_minimum_stops(self, stops: QuerySet):
        if len(stops) < 2:
            raise ValidationError('A bus shift requires at least two stops.')

    def check_bus_overlaps(self, start: datetime, end: datetime, bus: Bus) -> None:
        overlapping = BusShift.objects.filter(bus=bus).filter(
            Q(stops__passage_datetime__range=(start, end)) |
            Q(stops__passage_datetime__lt=start, stops__passage_datetime__gt=end)
        )
        if overlapping.exists():
            raise ValidationError('This bus is already scheduled for a shift during the selected time.')

    def check_driver_overlaps(self, start: datetime, end: datetime, driver: Driver) -> None:
        overlapping = BusShift.objects.filter(driver=driver).filter(
            Q(stops__passage_datetime__range=(start, end)) |
            Q(stops__passage_datetime__lt=start, stops__passage_datetime__gt=end)
        )
        if overlapping.exists():
            raise ValidationError('This driver is already assigned to another shift during the selected time.')
