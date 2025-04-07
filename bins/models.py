from django.db import models

# Create your models here.
class BinModel(models.Model):
    id = models.UUIDField(primary_key=True)
    location = models.CharField(max_length=100)
    emptied_at = models.DateTimeField(null=True)
    fill_level = models.FloatField()


# class BinLocation(models.Model):
#     id = models.UUIDField(primary_key=True)
#     location = models.CharField(max_length=100)
#     number_of_bins = models.BigIntegerField(null=False)
#     date_emptied = models