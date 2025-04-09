from django.db import models

# Create your models here.

class BinLocationModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    capacity = models.IntegerField()

class BinModel(models.Model):
    id = models.UUIDField(primary_key=True)
    location = models.ForeignKey(
        BinLocationModel,
        on_delete=models.CASCADE,
        related_name="bins"
    )
    bin_url = models.CharField(max_length=150, default=None)
    emptied_at = models.DateTimeField(null=True)