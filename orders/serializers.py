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


class PriceListRecommendationSerializer(serializers.Serializer):
    sku_id = serializers.CharField()
    supplier_id = serializers.CharField()
    stock = serializers.IntegerField()
    price_recommended = serializers.FloatField()


class QuotationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    customer_id = serializers.CharField()
    sku_id = serializers.CharField()
    quantity = serializers.IntegerField()
    uom_id = serializers.CharField()
    recommendation = PriceListRecommendationSerializer(many=True)


class HistoricalPriceSerializers(serializers.ModelSerializer):
    order_items = QuotationItemsReadSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['id', 'customer_id', 'status', 'order_items']
