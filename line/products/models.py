from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'

    def __str__(self):
        return self.name


class File(models.Model):

    type = models.CharField(max_length=10, verbose_name="Тип файла")
    file = models.ImageField(
        upload_to=lambda instance, filename: '/'.join(['users', 'product', str(instance.type), filename])
    )
    size = models.CharField(max_length=10, verbose_name="размер файла")
    name = models.CharField(max_length=10, verbose_name="Имя файла")

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.file


class Product(models.Model):

    product_type = models.ForeignKey(ProductType, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    title = models.CharField(max_length=255, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", null=True)
    file = models.ForeignKey(File, models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    year_issue = models.DateTimeField(verbose_name="Год выпуска")

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

