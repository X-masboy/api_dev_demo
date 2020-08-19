from django.db import models


class AdvertisingData(models.Model):

    date = models.DateField(
        verbose_name="Date"
    )
    channel = models.CharField(max_length=255)
    country = models.CharField(max_length=5)
    os = models.CharField(max_length=255)
    impressions = models.PositiveIntegerField()
    clicks = models.PositiveIntegerField()
    installs = models.PositiveIntegerField()
    spend = models.FloatField()
    revenue = models.FloatField()

    class Meta:
        verbose_name = "AdvertisingData"
        verbose_name_plural = "AdvertisingData"

    def __str__(self):
        return self.channel

