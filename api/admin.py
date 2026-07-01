from django.contrib import admin
from .models import Locations, UserProfiles, EventOrganizers, Bookings


admin.site.register(Locations)
admin.site.register(UserProfiles)
admin.site.register(EventOrganizers)
admin.site.register(Bookings)
