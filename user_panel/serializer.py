from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'email', 'phone_number', 'address', 'profile_image']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']