from django.contrib import admin
from .models import Website, Product, Price


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'website', 'interval']


class PriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'date']


admin.site.register(Website)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price, PriceAdmin)
