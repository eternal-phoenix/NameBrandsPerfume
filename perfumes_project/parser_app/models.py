from django.db import models

# Create your models here.

class Item(models.Model):
    url = models.CharField(max_length=510)
    category = models.TextField()
    name = models.TextField()
    description = models.TextField()
    sku = models.CharField(max_length=510)