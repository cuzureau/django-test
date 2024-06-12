import random

from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.ride.factories import BusShiftFactory, BusStopFactory

class Command(CreateDataBaseCommand):
    help = 'Create few bus shifts with a few bus stops associated'

    def handle(self, *args, **options):
        super().handle(*args, **options)
        for _ in range(self.number):
            stops_count = random.randint(2, 12)
            stops = self.create_bus_stops(stops_count)
            shift = self.create_bus_shift_with_stops(stops)
            self.stdout.write(f'Created BusShift {shift.pk} with {stops_count} stops')

    @staticmethod
    def create_bus_stops(count: int):
        return BusStopFactory.create_batch(count)

    @staticmethod
    def create_bus_shift_with_stops(stops):
        shift = BusShiftFactory()
        shift.stops.set(stops)
        shift.save()
        return shift
