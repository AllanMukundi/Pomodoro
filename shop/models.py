from django.db import models

class Item(models.Model):
    perk = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField(default=0)


