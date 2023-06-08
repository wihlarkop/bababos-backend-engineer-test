from django.db.models.query import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from core.utils import JsonResponse
from product.models import PriceList
from product.serializers import PriceListFilter, PriceListReadSerializer, PriceListWriteSerializer


class PriceListsView(APIView):
    serializers_read = PriceListReadSerializer
    serializers_write = PriceListWriteSerializer
    model = PriceList

    @swagger_auto_schema(
        operation_id='price_list',
        operation_description="get all price list",
        manual_parameters=[
            openapi.Parameter(
                name='supplier_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Supplier ID',
                required=False,
            ),
            openapi.Parameter(
                name='sku_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='SKU ID',
                required=False,
            ),
            openapi.Parameter(
                name='price_lte',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Price Lower Then Equal',
                required=False,
            ),
            openapi.Parameter(
                name='price_gt',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Price Greater Then',
                required=False,
            ),
            openapi.Parameter(
                name='stock_lte',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Stock Lower Then Equal',
                required=False,
            ),
            openapi.Parameter(
                name='stock_gt',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Stock Greater Then',
                required=False,
            ),
        ],
        responses={200: openapi.Response("success response", serializers_read(many=True))},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request) -> JsonResponse:
        data: QuerySet = self.model.objects.select_related('supplier_id', 'sku_id')

        price_list_filter = PriceListFilter(instance=request.query_params)

        supplier_id: str = price_list_filter.instance.get('supplier_id')
        sku_id: str = price_list_filter.instance.get('sku_id')
        price_lte: str = price_list_filter.instance.get('price_lte')
        price_gt: str = price_list_filter.instance.get('price_gt')
        stock_lte: str = price_list_filter.instance.get('stock_lte')
        stock_gt: str = price_list_filter.instance.get('stock_gt')

        if supplier_id:
            data = data.filter(supplier_id__supplier_id__icontains=supplier_id)

        if sku_id:
            data = data.filter(sku_id__sku_id=sku_id)

        if price_gt:
            data = data.filter(price__gt=price_gt)

        if price_lte:
            data = data.filter(price__lte=price_lte)

        if stock_gt:
            data = data.filter(stock__gt=stock_gt)

        if stock_lte:
            data = data.filter(stock__lte=stock_lte)

        serializer = self.serializers_read(instance=data, many=True)
        return JsonResponse(data=serializer.data)

    @swagger_auto_schema(
        operation_id='price_list_create',
        operation_description="create price list",
        request_body=serializers_write,
        responses={201: openapi.Response("success add price list")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def post(self, request: Request) -> JsonResponse:
        data = request.data
        serializer = self.serializers_write(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return JsonResponse(message="success add price list")


class PriceListView(APIView):
    serializers_read = PriceListReadSerializer
    serializers_write = PriceListWriteSerializer
    model = PriceList

    def get_object(self, price_list_id):
        try:
            return self.model.objects.get(id=price_list_id)
        except self.model.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_id='price_list_detail',
        responses={200: openapi.Response("success response", serializers_read)},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request, price_list_id: str) -> JsonResponse:
        price_list = self.get_object(price_list_id=price_list_id)
        if price_list:
            serializer = self.serializers_read(instance=price_list)
            return JsonResponse(data=serializer.data)
        return JsonResponse(message='price list not found')

    @swagger_auto_schema(
        operation_id='price_list_update',
        request_body=serializers_write,
        responses={200: openapi.Response("success update price list")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def put(self, request: Request, price_list_id: str):
        price_list = self.get_object(price_list_id=price_list_id)
        if price_list:
            serializer = self.serializers_write(price_list, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.update(price_list, serializer.validated_data)
                return JsonResponse(message="success update price list")
        return JsonResponse(message='price list not found', status_code=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_id='price_list_delete',
        responses={200: openapi.Response("success delete price list")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def delete(self, request: Request, price_list_id: str):
        price_list = self.get_object(price_list_id=price_list_id)
        if price_list:
            price_list.delete()
            return JsonResponse(message="success delete price list", status_code=HTTP_204_NO_CONTENT)
        return JsonResponse(message='price list not found', status_code=HTTP_404_NOT_FOUND)