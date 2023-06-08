from django.db import models

ACCEPTED = "Accepted"
PENDING = "Pending"
DECLINE = "Decline"


class Orders(models.Model):
    STATUS_ORDERS = [
        (ACCEPTED, "Accepted"),
        (PENDING, "Pending"),
        (DECLINE, "Decline"),
    ]

    customer_id = models.ForeignKey(to='customer.Customer', on_delete=models.CASCADE)
    order_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, default=PENDING, choices=STATUS_ORDERS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'


class OrderItems(models.Model):
    order_id = models.ForeignKey(to='orders.Orders', on_delete=models.CASCADE)
    sku_id = models.ForeignKey(to='product.Sku', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    uom_id = models.ForeignKey(to='product.UnitOfMeasure', on_delete=models.CASCADE)
    unit_selling_price = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_items'
