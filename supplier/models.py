from django.db import models


class Supplier(models.Model):
    supplier_id = models.CharField(max_length=10, unique=True, primary_key=True)
    address = models.TextField()
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.supplier_id}'

    class Meta:
        db_table = 'supplier'


class Fleet(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    capacity = models.IntegerField()
    uom_id = models.ForeignKey(to='product.UnitOfMeasure', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'fleet'


class Logistic(models.Model):
    fleet_type = models.ForeignKey(to='supplier.Fleet', on_delete=models.CASCADE)
    origin = models.CharField(max_length=15)
    destination = models.CharField(max_length=15)
    price = models.IntegerField()

    class Meta:
        db_table = 'logistic'
