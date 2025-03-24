from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import BlacklistedToken

class BlacklistMiddleware(MiddlewareMixin):
    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            if BlacklistedToken.objects.filter(token=token).exists():
                return JsonResponse({"detail": "Unauthorized."}, status=401)
        response = self.get_response(request)
        return response