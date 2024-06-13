from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import APIToken,EmailModel
from rest_framework import status
from datetime import datetime, timedelta
from .serializers import APITokenSerializer, EmailModelSerializer
import string
import secrets
from .utils import send_email


# Create your views here.

class CreateNewTokenView(APIView):
    def post(self, request, email):
        return self.create_token(request, email)

    def get(self, request, email):
        return self.create_token(request, email)

    def create_token(self, request, email):
        try:
            existing_token = APIToken.objects.filter(email__email=email, active=True).first()
            if existing_token:
                return Response({"message": "Active token already exists for this email"}, status=status.HTTP_400_BAD_REQUEST)
            email_instance, created = EmailModel.objects.get_or_create(email=email)
            token = self.generate_token(length=30)
            expiry_date = datetime.now().date() + timedelta(days=365)
            api_token = APIToken.objects.create(
                email=email_instance,
                token=token,
                expiry_date=expiry_date,
                active=True,
            )
            subject = 'API Token'
            message = f'Hi,\nPlease find your token below:\n\nToken: {token}\n\nUse this token to access our API.'
            recipient_list = [email]
            send_email(subject, message, recipient_list)
            serializer = APITokenSerializer(api_token)
            return Response({"message": "Token created successfully. Please check your email."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_token(self, length=30):
        import secrets
        import string
        alphabet = string.ascii_letters
        digits = string.digits
        combined_characters = alphabet + digits
        token = ''.join(secrets.choice(combined_characters) for _ in range(length))
        return token

