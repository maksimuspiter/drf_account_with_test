from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import AccountFullSerializer, CreateAccountSerializer, UserSerializer
from .models import Account


class AccountForUserViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountFullSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["create"] and self.request.user.is_superuser:
            return CreateAccountSerializer
        return self.serializer_class


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdminUser,
    ]
