from rest_framework import serializers

from customer.models import Customer


class CustomerFilter(serializers.Serializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'city', 'state']
