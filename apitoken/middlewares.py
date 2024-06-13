from django.http import JsonResponse
from django.utils import timezone
from .models import APIToken

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.should_exclude_validation(request.path_info):
            response = self.get_response(request)
            return response

        token = request.GET.get('API_TOKEN')

        if not token or not self.is_valid_token(token):
            return JsonResponse({'error': 'Invalid or missing API token'}, status=401)

        response = self.get_response(request)
        return response

    def should_exclude_validation(self, path_info):
        excluded_patterns = ['/apitoken/getapitoken/', '/admin/']
        for pattern in excluded_patterns:
            if pattern in path_info:
                return True
        return False

    def is_valid_token(self, token):
        try:
            api_token = APIToken.objects.get(token=token)
            if not api_token.active or api_token.expiry_date < timezone.now().date():
                return False
            return True
        except APIToken.DoesNotExist:
            return False
