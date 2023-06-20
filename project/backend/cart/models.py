from django.db import models
from users.models import Account
from shop.models import Product


class Cart(models.Model):
    customer = models.OneToOneField(
        Account,
        related_name="cart",
        verbose_name="Покупатель",
        on_delete=models.CASCADE,
    )
    total_price = models.DecimalField(
        verbose_name="Цена", max_digits=8, decimal_places=2, default=0
    )
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def update_total_price(self):
        self.total_price = sum(item.get_total_price() for item in self.items.all())
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_price = sum(item.get_total_price() for item in self.items.all())
        super().save()

    def __str__(self) -> str:
        return f"{self.id}: {self.customer.user} (paid: {self.paid})"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name="items", on_delete=models.CASCADE, verbose_name="Корзина"
    )
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество", default=1)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def get_total_price(self):
        return self.product.price_now * self.quantity

    def __str__(self) -> str:
        return f"{self.id}: {self.product.title} -- {self.quantity}"
