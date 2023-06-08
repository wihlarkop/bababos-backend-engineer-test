from django.contrib import admin

from product.models import Sku, PriceList, UnitOfMeasure


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier_id', 'sku_id', 'price', 'stock']


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    pass


@admin.register(UnitOfMeasure)
class UnitOfMeasure(admin.ModelAdmin):
    pass
