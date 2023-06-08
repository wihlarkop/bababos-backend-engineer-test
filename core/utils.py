import typing

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def JsonResponse(
        data: typing.Any = None,
        message: str = 'Success',
        status_code: status = status.HTTP_200_OK,
        success: bool = True,
        meta=None,
) -> Response:
    if meta is None:
        meta = {}

    response_data = {
        'data': data,
        'message': message,
        'meta': meta,
        'success': success
    }

    response = Response(response_data, status=status_code)
    renderer = JSONRenderer()
    renderer_context = {'indent': 4}
    response.accepted_renderer = renderer
    response.accepted_media_type = "application/json"
    response.renderer_context = renderer_context
    return response.render()
