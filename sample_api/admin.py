from django.contrib import admin

from .models import AdvertisingData


class AdvertisingDataAdmin(admin.ModelAdmin):

    list_display = ('date', 'channel', 'country', 'os', 'impressions', 'clicks', 'installs', 'spend', 'revenue',)
    list_filter = ('channel', 'country', 'os',)


admin.site.register(AdvertisingData, AdvertisingDataAdmin)
