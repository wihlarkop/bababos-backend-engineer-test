from django.db.models.query import QuerySet

from rest_framework.request import Request
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.utils import JsonResponse
from customer.filter import CustomerFilter
from customer.models import Customer
from customer.serializers import CustomerSerializer


class CustomersView(APIView):
    serializers = CustomerSerializer
    model = Customer

    @swagger_auto_schema(
        operation_id='customer_list',
        operation_description="get all customer",
        manual_parameters=[
            openapi.Parameter(
                name='customer_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Customer ID',
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

        customer_filter = CustomerFilter(instance=request.query_params)

        customer_id: str = customer_filter.instance.get('customer_id')
        city: str = customer_filter.instance.get('city')
        state: str = customer_filter.instance.get('state')

        if city:
            data = data.filter(city__icontains=city)

        if state:
            data = data.filter(state__icontains=state)

        if customer_id:
            data = data.filter(customer_id=customer_id)

        serializer = self.serializers(instance=data, many=True)
        return JsonResponse(data=serializer.data)

    @swagger_auto_schema(
        operation_id='customer_create',
        operation_description="create customer",
        request_body=serializers,
        responses={201: openapi.Response("success add customer")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def post(self, request: Request) -> JsonResponse:
        data = request.data
        serializer = self.serializers(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return JsonResponse(message="success add customer", status_code=HTTP_201_CREATED)


class CustomerView(APIView):
    serializer = CustomerSerializer
    model = Customer

    def get_object(self, customer_id):
        try:
            return self.model.objects.get(customer_id=customer_id)
        except self.model.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_id='customer_detail',
        responses={200: openapi.Response("success response", serializer)},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request, customer_id: str) -> JsonResponse:
        customer = self.get_object(customer_id=customer_id)
        if customer:
            serializer = self.serializer(instance=customer)
            return JsonResponse(data=serializer.data)
        return JsonResponse(message='customer not found')

    @swagger_auto_schema(
        operation_id='customer_update',
        request_body=serializer,
        responses={200: openapi.Response("success update customer")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def put(self, request: Request, customer_id: str):
        customer = self.get_object(customer_id)
        if customer:
            if 'customer_id' in request.data:
                request.data.pop('customer_id')

            serializer = CustomerSerializer(customer, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.update(customer, serializer.validated_data)
                return JsonResponse(message="success update customer")
        return JsonResponse(message='customer not found', status_code=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_id='customer_delete',
        responses={200: openapi.Response("success delete customer")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def delete(self, request: Request, customer_id: str):
        customer = self.get_object(customer_id)
        if customer:
            customer.delete()
            return JsonResponse(message="success delete customer", status_code=HTTP_204_NO_CONTENT)
        return JsonResponse(message='customer not found', status_code=HTTP_404_NOT_FOUND)
