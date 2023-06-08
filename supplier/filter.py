from rest_framework import serializers


class SupplierFilter(serializers.Serializer):
    class Meta:
        fields = ['supplier_id', 'city', 'state']


class LogisticFilter(serializers.Serializer):
    class Meta:
        fields = ['fleet_type', 'origin', 'destination']
