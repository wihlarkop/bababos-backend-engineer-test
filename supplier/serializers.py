from rest_framework import serializers

from supplier.models import Supplier, Logistic, Fleet


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['supplier_id', 'address', 'city', 'state']


class LogisticReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logistic
        fields = ['id', 'fleet_type', 'origin', 'destination', 'price']


class LogisticWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logistic
        fields = ['fleet_type', 'origin', 'destination', 'price']
