from rest_framework import serializers

from orders.models import Orders


class QuotationFilter(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['customer_id', 'sku_id', 'quantity', 'uom_id']
