from django.urls import path

from supplier.views import SuppliersView, SupplierView, LogisticsView, LogisticView

app_name = "supplier"

urlpatterns = [
    path('', SuppliersView.as_view()),
    path('<str:supplier_id>', SupplierView.as_view()),

    path('logistic/', LogisticsView.as_view()),
    path('logistic/<int:logistic_id>', LogisticView.as_view())
]
