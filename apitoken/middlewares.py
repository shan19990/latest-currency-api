from django.http import JsonResponse
from django.utils import timezone
from .models import APIToken, DailyTokenUsage

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path should be excluded from validation
        if self.should_exclude_validation(request.path_info):
            return self.get_response(request)

        token = request.GET.get('API_TOKEN')

        # Validate token
        if not token or not self.is_valid_token(token):
            return JsonResponse({'error': 'Invalid or missing API token'}, status=401)

        # Check daily usage limit
        if not self.can_use_token(token):
            return JsonResponse({'error': 'Daily usage limit exceeded'}, status=429)

        # Attach token to request for use in process_response
        request.api_token = token

        # Process the request
        response = self.get_response(request)

        # Update daily usage only if the response is successful
        if response.status_code == 200:
            self.update_daily_usage(token)

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

    def can_use_token(self, token):
        today = timezone.now().date()
        try:
            api_token = APIToken.objects.get(token=token)
            daily_usage, created = DailyTokenUsage.objects.get_or_create(token=api_token, date=today)
            if daily_usage.usage_count >= 200:
                return False
            return True
        except APIToken.DoesNotExist:
            return False

    def update_daily_usage(self, token):
        today = timezone.now().date()
        try:
            api_token = APIToken.objects.get(token=token)
            daily_usage, created = DailyTokenUsage.objects.get_or_create(token=api_token, date=today)
            daily_usage.usage_count += 1
            daily_usage.save()
        except APIToken.DoesNotExist:
            pass
