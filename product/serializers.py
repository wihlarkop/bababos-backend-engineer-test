from rest_framework import serializers

from product.models import PriceList


class PriceListReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = ['id', 'supplier_id', 'sku_id', 'price', 'stock']


class PriceListWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = ['supplier_id', 'sku_id', 'price', 'stock']


class PriceListFilter(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = ['supplier_id', 'sku_id', 'price_lt', 'price_gt', 'stock_lt', 'stock_gt']
