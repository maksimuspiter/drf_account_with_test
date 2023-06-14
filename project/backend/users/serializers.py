from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class AccountFullSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ["id", "nickname", "user", "get_absolute_url", "get_user_url"]


class CreateAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    password = serializers.CharField(source="user.password")

    class Meta:
        model = Account
        fields = (
            "username",
            "password",
            "nickname",
        )
        related_fields = ["user"]

    def create(self, validated_data):
        username = self.validated_data["user"]["username"]
        password = self.validated_data["user"]["password"]

        nickname = self.validated_data["nickname"]

        account = Account.objects.create_account(
            username=username, password=password, nickname=nickname
        )
        return account
