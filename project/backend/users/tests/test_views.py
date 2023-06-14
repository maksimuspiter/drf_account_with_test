from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.models import Account


class AccountForAdminTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="test_user")
        user.set_password("secret")
        user.save()
        admin = User.objects.create_superuser(username="test_admin", password="secret")
        Account.objects.create(user=user, nickname="SimpleUser")
        Account.objects.create(user=admin, nickname="TheBestUser")

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_get_list_by_admin(self):
        self.client.login(username="test_admin", password="secret")
        response = self.client.get("/api-users/accounts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_list_by_simple_user(self):
        self.client.login(username="test_user", password="secret")
        response = self.client.get("/api-users/accounts/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_or_retrieve_by_unauthorized_user(self):
        response = self.client.get("/api-users/accounts/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get("/api-users/accounts/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_retrieve_by_admin(self):
        new_account = Account.objects.create_account(
            username="new_user", password="secret"
        )

        self.client.login(username="test_admin", password="secret")
        response = self.client.get(f"/api-users/accounts/{new_account.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": new_account.pk,
                "nickname": None,
                "user": {
                    "id": new_account.user.pk,
                    "username": new_account.user.username,
                },
                "get_absolute_url": f"http://127.0.0.1:8000/api-users/accounts/{new_account.pk}/",
                "get_user_url": f"http://127.0.0.1:8000/api-users/users/{new_account.user.pk}/",
            },
        )

    def test_get_retrieve_by_simple_user(self):
        new_account = Account.objects.create_account(
            username="new_user2", password="secret"
        )

        self.client.login(username="test_user", password="secret")
        response = self.client.get(f"/api-users/accounts/{new_account.pk}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_account_by_admin(self):
        self.client.login(username="test_admin", password="secret")

        data = {
            "username": "new_created_user1",
            "password": "secret",
            "nickname": "new_created_user1_nick",
        }

        response = self.client.post("/api-users/accounts/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json().get("username"), "new_created_user1")
        self.assertEqual(response.json().get("nickname"), "new_created_user1_nick")

    def test_create_account_by_simple_user(self):
        self.client.login(username="test_user", password="secret")
        data = {
            "username": "test_data",
            "password": "test_data",
            "nickname": "test_data",
        }

        response = self.client.post("/api-users/accounts/", data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
