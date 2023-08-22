from django.contrib import admin
from parser_app import models
# Register your models here.

@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('url', 'category', 'name', 'description', 'sku')