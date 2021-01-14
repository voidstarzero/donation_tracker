from django.contrib import admin

from . import models

# Registrations for models needed in the admin panel
admin.site.register(models.Club)
admin.site.register(models.Balance)
admin.site.register(models.Attendee)
admin.site.register(models.Event)
admin.site.register(models.Donation)
