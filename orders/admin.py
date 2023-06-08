from django.contrib import admin

from orders.models import Orders, OrderItems


class OrderItemInline(admin.StackedInline):
    model = OrderItems
    extra = 0


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'order_date']
    inlines = [OrderItemInline]
