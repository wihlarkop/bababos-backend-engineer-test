from http import HTTPStatus
from typing import Any

from django.http import HttpRequest
from rest_framework.views import exception_handler

from core.utils import JsonResponse


class JSONErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.status_code_description = {
            v.value: v.description for v in HTTPStatus
        }

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)

        if not request.content_type == "application/json":
            return response

        status_code = response.status_code
        if not HTTPStatus.BAD_REQUEST < status_code <= HTTPStatus.INTERNAL_SERVER_ERROR:
            return response

        return JsonResponse(status_code=status_code, message=self.status_code_description[status_code]).render()


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> JsonResponse:
    response = exception_handler(exc, context)
    status_code = response.status_code
    message = response.data

    return JsonResponse(status_code=status_code, message=message, success=False)
