from django.db import models, IntegrityError
from django.contrib.auth.models import User


class EmailAlreadyExist(Exception):
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
        except IntegrityError as e:
            raise EmailAlreadyExist("Такой email уже используются")


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

    objects = AccountManager()

    class Meta:
        ordering = ["-created"]
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self):
        return f"Аккаунт: {self.user.username}"
