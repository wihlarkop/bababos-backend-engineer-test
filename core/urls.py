from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bababos API",
        default_version='v1',
        description="Backend Engineer test for bababos",
    ),
    public=True,
)

urlpatterns = [
    re_path(r'^$', schema_view.with_ui('swagger'), name='swagger-ui'),

    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),

    path('api/v1/customer/', include('customer.urls')),
    path('api/v1/supplier/', include('supplier.urls')),
    path('api/v1/product/', include('product.urls')),
    path('api/v1/orders/', include('orders.urls')),
]
