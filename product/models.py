from django.db import models


class Sku(models.Model):
    sku_id = models.CharField(max_length=20, unique=True, primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sku_id}'

    class Meta:
        db_table = 'sku'


class PriceList(models.Model):
    sku_id = models.ForeignKey(to='product.Sku', to_field='sku_id', on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(to='supplier.Supplier', on_delete=models.CASCADE)
    price = models.FloatField()
    stock = models.IntegerField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'price_list'


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'uom'
