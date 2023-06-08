from django.contrib import admin

from supplier.models import Supplier, Fleet, Logistic


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['supplier_id', 'address', 'city', 'state']


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'uom_id']


@admin.register(Logistic)
class LogisticAdmin(admin.ModelAdmin):
    list_display = ['id', 'fleet_type', 'origin', 'destination', 'price']
