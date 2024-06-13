# api/serializers.py
from rest_framework import serializers
from .models import APIToken, EmailModel

class EmailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailModel
        fields = ('id', 'email')


class APITokenSerializer(serializers.ModelSerializer):
    email = serializers.PrimaryKeyRelatedField(queryset=EmailModel.objects.all())

    class Meta:
        model = APIToken
        fields = ('id', 'email', 'token', 'created_at', 'expiry_date', 'active')

    def create(self, validated_data):
        return APIToken.objects.create(**validated_data)
