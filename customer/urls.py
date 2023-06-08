from django.urls import path

from customer.views import CustomersView, CustomerView

app_name = "customer"

urlpatterns = [
    path('', CustomersView.as_view()),
    path('<str:customer_id>', CustomerView.as_view())
]
