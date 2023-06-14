from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class AccountFullSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ["id", "nickname", "user", "get_absolute_url", "get_user_url"]


class AccountSimpleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    password = serializers.CharField(source="user.password")

    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "password",
            "nickname",
        )
        related_fields = ["user"]


class CreateAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
    )
    password = serializers.CharField(
        source="user.password",
        write_only=True,
        required=False,
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = Account
        fields = (
            "username",
            "password",
            "nickname",
        )
        related_fields = ["user"]

    def create(self, validated_data, format="json"):
        username = self.validated_data["user"]["username"]
        password = self.validated_data["user"]["password"]
        nickname = self.validated_data["nickname"]
        account = Account.objects.create_account(
            username=username, password=password, nickname=nickname
        )
        return account

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.user.username = validated_data.get("user", instance.user)["username"]

        user = validated_data.get("user")
        if user and user.get("password"):
            instance.user.password = make_password(user.get("password"))

        instance.save()
        return instance
