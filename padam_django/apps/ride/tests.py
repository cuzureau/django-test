from django.test import TestCase

from ..fleet.factories import BusFactory, DriverFactory
from .forms import BusShiftForm
from .factories import BusStopFactory


class BusShiftTestCase(TestCase):

    def setUp(self):
        self.bus = BusFactory()
        self.driver = DriverFactory()

    def test_single_stop_error(self):
        stop1 = BusStopFactory.create_batch(1)
        form = BusShiftForm(data={
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'stops': [stop1.pk],
        })

        self.assertFalse(form.is_valid())
        self.assertIn('At least two stops are required', form.errors['__all__'])
