from itertools import groupby
from statistics import linear_regression

from django.db.models import F
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from core.utils import JsonResponse
from orders.filter import QuotationFilter
from orders.models import Orders, ACCEPTED, PENDING, OrderItems
from orders.serializers import (
    QuotationReadSerializer,
    QuotationWriteSerializer,
    HistoricalPriceSerializers,
)


class QuotationsView(APIView):
    serializers_read = QuotationReadSerializer
    serializers_write = QuotationWriteSerializer
    model = Orders

    @swagger_auto_schema(
        operation_id='quotation_list',
        operation_description="get all quotation list",
        manual_parameters=[
            openapi.Parameter(
                name='customer_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Customer ID',
                required=False,
            ),
            openapi.Parameter(
                name='sku_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='SKU ID',
                required=False,
            )
        ],
        responses={200: openapi.Response("success response", serializers_read(many=True))},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request) -> JsonResponse:
        quotation = QuotationFilter(instance=request.query_params)

        data = self.model.objects.select_related(
            'customer_id',
        ).only(
            'id',
            'customer_id',
        ).filter(status=PENDING)

        customer_id: str = quotation.instance.get('customer_id')
        if customer_id:
            data = data.filter(customer_id=customer_id)

        sku_id: str = quotation.instance.get('sku_id')
        if sku_id:
            data = data.filter(sku_id=sku_id)

        serializer = self.serializers_read(instance=data, many=True)
        return JsonResponse(data=serializer.data)

    # def post(self, request: Request) -> JsonResponse:
    #     data = request.data
    #     serializer = self.serializers_write(data=data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #     return JsonResponse(message="success add quotation")


class QuotationView(APIView):
    model = Orders

    def get_object(self, quotation_id):
        try:
            return Orders.objects.get(id=quotation_id)
        except self.model.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_id='quotation_detail',
        responses={200: openapi.Response("success response")},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request, quotation_id: str) -> JsonResponse:
        quotation = self.get_object(quotation_id)
        if not quotation:
            return JsonResponse(message='Quotation not found')

        quotation_items = quotation.orderitems_set.select_related('sku_id').only('sku_id', 'quantity').order_by(
            'sku_id')

        sku_ids = quotation_items.values_list('sku_id', flat=True)

        history_price_queryset = OrderItems.objects.filter(
            order_id__status='Accepted',
            sku_id__in=sku_ids
        ).annotate(
            total_price=F('quantity') * F('unit_selling_price')
        ).order_by('sku_id', 'total_price').values('sku_id', 'quantity', 'total_price')

        history_price = []
        for sku_id, items in groupby(history_price_queryset, key=lambda x: x.get('sku_id')):
            quantity = []
            total_price = []
            for item in items:
                quantity.append(item.get('quantity'))
                total_price.append(item.get('total_price'))

            history_price.append({
                'sku_id': sku_id,
                'quantity': quantity,
                'total_price': total_price
            })

        order_items = []

        for item in quotation_items:
            new_x = item.quantity  # quantity yang di request

            for history in history_price:
                x = history.get('quantity')  # quantity
                y = history.get('total_price')  # price
                sku_id = history.get('sku_id')

                if item.sku_id.sku_id == sku_id:
                    if len(x) != 1:
                        gradient, intercept = linear_regression(x, y)

                        predicted_y = gradient * new_x + intercept
                        rounded_predicted_y = round(predicted_y, 2)

                        if y[0] <= rounded_predicted_y <= y[-1]:
                            rounded_predicted_y = y[0]
                        else:
                            rounded_predicted_y = y[-1]

                        order_items.append({
                            "product": sku_id,
                            "quantity": new_x,
                            "price": rounded_predicted_y
                        })
                    else:
                        order_items.append({
                            "product": sku_id,
                            "quantity": new_x,
                            "price": round(y[0], 2)
                        })

        result = {
            "id": quotation.id,
            "customer_id": quotation.customer_id_id,
            "order_items": order_items
        }
        return JsonResponse(data=result)


class HistoricalPricesView(APIView):
    serializers = HistoricalPriceSerializers
    model = Orders

    @swagger_auto_schema(
        operation_id='history_order_list',
        operation_description="get all history order",
        tags=['history order'],
        responses={200: openapi.Response("success response", serializers(many=True))},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request) -> JsonResponse:
        histories = self.model.objects.select_related('customer_id').filter(status=ACCEPTED)

        data = []

        for history in histories:
            data.append({
                'id': history.id,
                'customer_id': history.customer_id,
                'status': history.status,
                'order_items': history.orderitems_set.all().only('sku_id', 'quantity', 'uom_id', 'unit_selling_price')
            })
        serializer = self.serializers(instance=data, many=True)
        return JsonResponse(data=serializer.data)


class HistoricalPriceView(APIView):
    serializer = HistoricalPriceSerializers
    model = Orders

    def get_object(self, history_id):
        try:
            return self.model.objects.select_related('customer_id').get(id=history_id)
        except self.model.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_id='history_order_detail',
        tags=['history order'],
        responses={200: openapi.Response("success response", serializer)},
        security=[{}]
        # security=[{"Bearer": {}}]
    )
    def get(self, request: Request, history_id: str) -> JsonResponse:
        quotation = self.get_object(history_id=history_id)
        order_items = quotation.orderitems_set.all()

        data = {
            'id': quotation.id,
            'customer_id': quotation.customer_id,
            'status': quotation.status,
            'order_items': order_items
        }

        serializer = self.serializer(instance=data)
        return JsonResponse(data=serializer.data)
