from django.http import JsonResponse
from django.middleware.common import MiddlewareMixin

from applications.common.utils.ip_address import IPBlock


class IPMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if IPBlock.check_ip_is_blocked(request=request):
            return JsonResponse(
                data={
                    "detail": "This IP blocked",
                    "code": "ip_blocked",
                    "error": "",
                    'data': {}
                },
                status=403)
