from django.contrib import admin

from apps.customers.models import Offers, Profiles

admin.site.register([Profiles, Offers])
