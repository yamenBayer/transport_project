from django.contrib import admin
from .models import Profile, Trip, Reservation

admin.site.register(Trip)
admin.site.register(Profile)
admin.site.register(Reservation)
