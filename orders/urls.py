from django.urls import path

from orders.views import QuotationView, QuotationsView, HistoricalPricesView, HistoricalPriceView

app_name = "orders"

urlpatterns = [
    path('quotation', QuotationsView.as_view()),
    path('quotation/<int:quotation_id>', QuotationView.as_view()),
    path('history', HistoricalPricesView.as_view()),
    path('history/<int:history_id>', HistoricalPriceView.as_view()),
]
