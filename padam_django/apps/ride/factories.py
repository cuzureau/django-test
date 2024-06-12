import random
from datetime import timedelta
from faker import Faker

import factory
from django.utils import timezone

from ..fleet.factories import BusFactory, DriverFactory
from ..geography.factories import PlaceFactory
from .models import BusShift, BusStop


fake = Faker(['fr'])


class BusStopFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.name)
    place = factory.SubFactory(PlaceFactory)
    passage_datetime = factory.LazyFunction(
        lambda: timezone.now() + timedelta(
            days=random.randint(-30, 30), 
            hours=random.randint(0, 23), 
            minutes=random.randint(0, 59))
    )

    class Meta:
        model = BusStop


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)

    class Meta:
        model = BusShift
