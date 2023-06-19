from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class AlreadyExist(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AccountManager(models.Manager):
    def create_account(self, username, password, nickname=None):
        try:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            account = self.model(user=user, nickname=nickname)
            account.save(using=self._db)
            return account
        except IntegrityError:
            raise AlreadyExist("Такой пользователь уже существует")


class Account(models.Model):
    nickname = models.CharField(
        max_length=255, verbose_name="Ник", null=True, blank=True
    )

    user = models.OneToOneField(
        User,
        related_name="account",
        verbose_name="пользователь",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="День рождения")

    avatar = models.ImageField(upload_to="uploads/avatar/", blank=True, null=True)
    objects = AccountManager()

    class Meta:
        ordering = ["-created"]
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self):
        return f"Аккаунт: {self.user.username}"

    def get_absolute_url(self):
        return "http://127.0.0.1:8000" + reverse_lazy(
            "users:accounts-detail", kwargs={"pk": self.pk}
        )

    def get_user_url(self):
        return "http://127.0.0.1:8000" + reverse_lazy(
            "users:users-detail", kwargs={"pk": self.user.pk}
        )

    def get_avatar(self):
        if self.avatar:
            return "http://127.0.0.1:8000" + self.avatar.url
        return "http://127.0.0.1:8000/static/images/base_avatar.webp"
