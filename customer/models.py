from django.db import models


class Customer(models.Model):
    customer_id = models.CharField(max_length=10, unique=True, primary_key=True)
    address = models.TextField()
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.customer_id}'

    class Meta:
        db_table = 'customer'
