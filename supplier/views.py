from django.db.models.query import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from core.utils import JsonResponse
from supplier.filter import SupplierFilter, LogisticFilter
from supplier.models import Supplier, Logistic
from supplier.serializers import SupplierSerializer, LogisticReadSerializer, LogisticWriteSerializer


class SuppliersView(APIView):
    serializers = SupplierSerializer
    model = Supplier

    @swagger_auto_schema(
        operation_id='supplier_list',
        operation_description="get all supplier",
        manual_parameters=[
            openapi.Parameter(
                name='supplier_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Supplier ID',
                required=False,
            ),
            openapi.Parameter(
                name='city',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='City',
                required=False,
            ),
            openapi.Parameter(
                name='state',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='State',
                required=False,
            ),
        ],
        responses={200: openapi.Response("success response", serializers(many=True))},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request) -> JsonResponse:
        data: QuerySet = self.model.objects.all()

        supplier_filter = SupplierFilter(instance=request.query_params)

        supplier_id: str = supplier_filter.instance.get('supplier_id')
        city: str = supplier_filter.instance.get('city')
        state: str = supplier_filter.instance.get('state')

        if supplier_id:
            data = data.filter(supplier_id=supplier_id)

        if city:
            data = data.filter(city__icontains=city)

        if state:
            data = data.filter(state__icontains=state)

        serializer = self.serializers(instance=data, many=True)
        return JsonResponse(data=serializer.data)

    @swagger_auto_schema(
        operation_id='supplier_create',
        operation_description="create supplier",
        request_body=serializers,
        responses={201: openapi.Response("success add supplier")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def post(self, request: Request) -> JsonResponse:
        data = request.data
        serializer = self.serializers(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return JsonResponse(message="success add supplier")


class SupplierView(APIView):
    serializer = SupplierSerializer
    model = Supplier

    def get_object(self, supplier_id):
        try:
            return self.model.objects.get(supplier_id=supplier_id)
        except self.model.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_id='supplier_detail',
        responses={200: openapi.Response("success response", serializer)},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request, supplier_id: str) -> JsonResponse:
        supplier = self.get_object(supplier_id=supplier_id)
        if supplier:
            serializer = self.serializer(instance=supplier)
            return JsonResponse(data=serializer.data)
        return JsonResponse(message='supplier not found')

    @swagger_auto_schema(
        operation_id='supplier_update',
        request_body=serializer,
        responses={200: openapi.Response("success update supplier")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def put(self, request: Request, supplier_id: str):
        supplier = self.get_object(supplier_id)
        if supplier:
            if 'supplier_id' in request.data:
                request.data.pop('supplier_id')

            serializer = self.serializer(supplier, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.update(supplier, serializer.validated_data)
                return JsonResponse(message="success update supplier")
        return JsonResponse(message='supplier not found', status_code=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_id='supplier_delete',
        responses={200: openapi.Response("success delete supplier")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def delete(self, request: Request, supplier_id: str):
        supplier = self.get_object(supplier_id)
        if supplier:
            supplier.delete()
            return JsonResponse(message="success delete supplier", status_code=HTTP_204_NO_CONTENT)
        return JsonResponse(message='supplier not found', status_code=HTTP_404_NOT_FOUND)


class LogisticsView(APIView):
    serializers_read = LogisticReadSerializer
    serializers_write = LogisticWriteSerializer
    model = Logistic

    @swagger_auto_schema(
        operation_id='logistic_list',
        operation_description="get all logistic",
        tags=['logistic'],
        manual_parameters=[
            openapi.Parameter(
                name='fleet_type',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Fleet Type',
                required=False,
            ),
            openapi.Parameter(
                name='origin',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Origin',
                required=False,
            ),
            openapi.Parameter(
                name='destination',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Destination',
                required=False,
            ),
        ],
        responses={200: openapi.Response("success response", serializers_read(many=True))},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request) -> JsonResponse:
        data = self.model.objects.all()

        logistic_filter = LogisticFilter(instance=request.query_params)

        fleet_type: str = logistic_filter.instance.get('fleet_type')
        origin: str = logistic_filter.instance.get('origin')
        destination: str = logistic_filter.instance.get('destination')

        if fleet_type:
            data = data.filter(fleet_type__name__icontains=fleet_type)

        if origin:
            data = data.filter(origin__icontains=origin)

        if destination:
            data = data.filter(destination__icontains=destination)

        serializer = self.serializers_read(instance=data, many=True)
        return JsonResponse(data=serializer.data)

    @swagger_auto_schema(
        operation_id='logistic_create',
        operation_description="create logistic",
        tags=['logistic'],
        request_body=serializers_write,
        responses={201: openapi.Response("success add logistic")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def post(self, request: Request) -> JsonResponse:
        data = request.data
        serializer = self.serializers_write(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return JsonResponse(message="success add logistic")


class LogisticView(APIView):
    serializers_read = LogisticReadSerializer
    serializers_write = LogisticWriteSerializer
    model = Logistic

    def get_object(self, logistic_id):
        try:
            return self.model.objects.get(id=logistic_id)
        except self.model.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_id='logistic_detail',
        tags=['logistic'],
        responses={200: openapi.Response("success response", serializers_read)},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request, logistic_id: int) -> JsonResponse:
        data = self.get_object(logistic_id)
        serializer = self.serializers_read(instance=data)
        return JsonResponse(data=serializer.data)

    @swagger_auto_schema(
        operation_id='logistic_update',
        tags=['logistic'],
        request_body=serializers_write,
        responses={200: openapi.Response("success update logistic")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def put(self, request: Request, logistic_id: int):
        logistic = self.get_object(logistic_id)
        if logistic:
            serializer = self.serializers_write(logistic, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.update(logistic, serializer.validated_data)
                return JsonResponse(message="success update logistic")
        return JsonResponse(message='logistic not found', status_code=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_id='logistic_delete',
        tags=['logistic'],
        responses={200: openapi.Response("success delete logistic")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def delete(self, request: Request, logistic_id: int):
        logistic = self.get_object(logistic_id)
        if logistic:
            logistic.delete()
            return JsonResponse(message="success delete logistic", status_code=HTTP_204_NO_CONTENT)
        return JsonResponse(message='logistic not found', status_code=HTTP_404_NOT_FOUND)
