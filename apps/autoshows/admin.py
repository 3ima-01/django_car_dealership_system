from django.contrib import admin

from apps.autoshows.models import AutoShow, Discount, Sale, Stock

admin.site.register([AutoShow, Stock, Discount, Sale])
