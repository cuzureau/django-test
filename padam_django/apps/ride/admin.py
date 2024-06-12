from . import forms
from .models import BusShift, BusStop
from django.contrib import admin


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "passage_datetime")


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = forms.BusShiftForm
    list_display = ("bus", "driver", "departure_datetime", "arrival_datetime", "total_duration")
