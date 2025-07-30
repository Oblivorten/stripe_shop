from django.contrib import admin
from .models import Item, Order, Discount, Tax

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'price', 'currency']
    list_filter = ['name', 'price']
    search_fields = ['name']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage']
    search_fields = ['name']

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'discount', 'tax']
    search_fields = ['id']
    filter_horizontal = ['items']