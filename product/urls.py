from django.urls import path

from product.views import PriceListView, PriceListsView

app_name = "product"

urlpatterns = [
    path('price-list', PriceListsView.as_view()),
    path('price-list/<int:price_list_id>', PriceListView.as_view()),
]
