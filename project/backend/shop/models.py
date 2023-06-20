from django.db import models


class Product(models.Model):
    title = models.CharField(verbose_name="Наименование", max_length=128)
    short_description = models.CharField(
        verbose_name="Краткое описание", max_length=1000, blank=True
    )
    description = models.TextField(verbose_name="Описание", blank=True)
    specifications = models.TextField(verbose_name="Характеристики", blank=True)
    price_now = models.DecimalField(
        verbose_name="Текущая цена", max_digits=8, decimal_places=2, default=0
    )
    price_old = models.DecimalField(
        verbose_name="Предыдущая цена", max_digits=8, decimal_places=2, default=0
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество на складе", default=0
    )

    category = models.ForeignKey(
        "Category",
        null=True,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        related_name="category",
    )
    image = models.ImageField(upload_to="uploads/products_images", blank=True)
    created = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name="Дата изменения",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def get_image_url(self):
        if self.image:
            return "http://127.0.0.1:8000" + self.image.url
        return "http://127.0.0.1:8000/static/images/base_product.webp"

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    title = models.CharField(
        verbose_name="Наименование категории", max_length=255, unique=True
    )
    description = models.TextField(
        verbose_name="Описание категории", max_length=500, blank=True
    )
    created = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name="Дата изменения",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Категория продуктов"
        verbose_name_plural = "Категории продуктов"

    def __str__(self):
        return self.title
