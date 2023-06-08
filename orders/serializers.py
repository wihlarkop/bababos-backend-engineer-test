from rest_framework import serializers

from orders.models import Orders, OrderItems


class QuotationItemsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['sku_id', 'quantity', 'uom_id']


class QuotationItemsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['sku_id', 'quantity', 'uom_id', 'unit_selling_price']


class QuotationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'customer_id']


class QuotationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['customer_id', 'sku_id', 'quantity', 'uom_id']


class HistoricalPriceSerializers(serializers.ModelSerializer):
    order_items = QuotationItemsReadSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['id', 'customer_id', 'status', 'order_items']
