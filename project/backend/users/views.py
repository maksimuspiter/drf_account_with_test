from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from .serializers import (
    AccountFullSerializer,
    AccountSimpleSerializer,
    CreateAccountSerializer,
    UserSerializer,
)
from .models import Account, AlreadyExist
from rest_framework.response import Response
from users.permissions import IsAccountOwnerOrAdmin


class AccountForAdminViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountFullSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["create"] and self.request.user.is_superuser:
            return CreateAccountSerializer
        return self.serializer_class


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    permission_classes = [IsAccountOwnerOrAdmin]
    serializer_class = AccountSimpleSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateAccountSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AlreadyExist as exception:
            return Response(
                {"created": False, "error": exception.message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError:
            return Response(
                {
                    "created": False,
                    "error": "Имя пользователя и пароль обязательные поля",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdminUser,
    ]
