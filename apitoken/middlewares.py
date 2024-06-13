# myapp/middlewares.py

from django.http import JsonResponse
from django.utils import timezone
from django.urls import resolve
from .models import APIToken

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request URL matches the exclusion pattern
        if self.should_exclude_validation(request.path_info):
            response = self.get_response(request)
            return response

        # Process the request before it reaches the view
        token = request.GET.get('API_TOKEN')

        # Check if token is present and valid
        if not token or not self.is_valid_token(token):
            return JsonResponse({'error': 'Invalid or missing API token'}, status=401)

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response

    def should_exclude_validation(self, path_info):
        # Define the exclusion pattern(s)
        excluded_patterns = ['/apitoken/getapitoken/', '/admin/']  # Adjust with your endpoint path

        # Check if the current request path matches any excluded pattern
        for pattern in excluded_patterns:
            if path_info.startswith(pattern):
                return True
        return False

    def is_valid_token(self, token):
        try:
            # Check if token exists and is active
            api_token = APIToken.objects.get(token=token)
            if not api_token.active or api_token.expiry_date < timezone.now().date():
                return False
            return True
        except APIToken.DoesNotExist:
            return False
