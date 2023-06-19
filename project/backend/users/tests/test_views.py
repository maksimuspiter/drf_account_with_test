from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.models import Account
from django.db import transaction


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
                "avatar": "http://127.0.0.1:8000/static/images/base_avatar.webp",
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


class AccountForSimpleUserTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Account.objects.create_account(
            username="test_user", password="secret", nickname="SimpleUser"
        )
        admin = User.objects.create_superuser(username="test_admin", password="secret")
        Account.objects.create(user=admin, nickname="TheBestUser")

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_non_authentication(self):
        response = self.client.get("/api-users/portfolio/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get("/api-users/portfolio/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post("/api-users/portfolio/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_user(self):
        self.client.login(username="test_user", password="secret")

        response = self.client.get("/api-users/portfolio/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get("/api-users/portfolio/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("username"), "test_user")

        response = self.client.get("/api-users/portfolio/2/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response

    def test_admin(self):
        self.client.login(username="test_admin", password="secret")

        response = self.client.get("/api-users/portfolio/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/api-users/portfolio/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_update_portfolio(self):
        user_data = {
            "username": "test_user_created1",
            "password": "secret",
            "nickname": "test1",
        }
        response = self.client.post("/api-users/portfolio/", data=user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with transaction.atomic():
            response = self.client.post("/api-users/portfolio/", data=user_data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                response.json(),
                {"created": False, "error": "Такой пользователь уже существует"},
            )
        user = User.objects.get(username="test_user_created1")

        new_user_data = {
            "username": "new_user",
        }
        response = self.client.put(
            f"/api-users/portfolio/{user.account.pk}/", data=new_user_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(username="test_user_created1", password="secret")

        response = self.client.put("/api-users/portfolio/1/", data=new_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test_admin", password="secret")
        admin_data = {
            "username": "changed_by_admin",
            "nickname": "changed_by_admin",
        }

        response = self.client.put(
            f"/api-users/portfolio/{user.account.pk}/",
            data=admin_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("username"), admin_data["username"])
        self.assertEqual(response.json().get("nickname"), admin_data["nickname"])

    def test_delete_portfolio(self):
        new_account = Account.objects.create_account(
            username="test_for_delete", password="secret"
        )
        new_account2 = Account.objects.create_account(
            username="test_for_delete2", password="secret"
        )
        response = self.client.delete("/api-users/portfolio/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(username="test_user", password="secret")

        response = self.client.delete(f"/api-users/portfolio/{new_account.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test_for_delete", password="secret")

        response = self.client.delete(f"/api-users/portfolio/{new_account.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.login(username="test_admin", password="secret")
        response = self.client.delete(f"/api-users/portfolio/{new_account2.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_portdolio_avatar(self):
        pass
