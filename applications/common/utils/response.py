from rest_framework.response import Response

from applications import OK_200


def custom_response(status_code: dict = OK_200, data: dict or list = None, error=None):
    return Response(
        data={
            'detail': status_code.get('detail'),
            'code': status_code.get('code', status_code.get('detail').replace(' ', '_')),
            'error': error,
            'data': data if data else {}
        },
        status=status_code.get('number'))
