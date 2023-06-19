from django.test import TestCase
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from users.models import Account, AlreadyExist


class CreateUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="test", password="12test12", email="test@example.com"
        )
        user.save()

    def test_correct(self):
        user = authenticate(username="test", password="12test12")
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username="wrong", password="12test12")
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username="test", password="wrong")
        self.assertFalse(user is not None and user.is_authenticated)


class CreateAccountTest(TestCase):
    def test_create_account(self):
        account = Account.objects.create_account(username="test_user1", password="test")

        user = User.objects.get(username="test_user1")
        self.assertTrue(user is not None and user.account == account)
        self.assertEqual(account.nickname, None)

        account2 = Account.objects.create_account(
            username="test@example.com", password="test", nickname="testNickname"
        )
        account2.save()
        self.assertTrue(account2.nickname == "testNickname")

        with transaction.atomic():
            try:
                Account.objects.create_account(
                    username="test@example.com",
                    password="test",
                    nickname="testNickname",
                )
            except AlreadyExist as exception:
                self.assertEqual(exception.message, "Такой пользователь уже существует")

    def test_account_avatar(self):
        account = Account.objects.create_account(
            username="test_user2", password="secret"
        )
        self.assertEqual(
            account.get_avatar(), "http://127.0.0.1:8000/static/images/base_avatar.webp"
        )
