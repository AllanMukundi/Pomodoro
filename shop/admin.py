from django.contrib import admin
from .models import Item

class ShopAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('perk', 'price')
    can_delete = False
    verbose_name_plural = 'Items'

admin.site.register(Item, ShopAdmin)
