from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории:')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название продукта:')
    description = models.TextField(verbose_name='Описание:')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена:')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='категория:')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Review(models.Model):
    text = models.TextField(verbose_name='Отзыв:')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Продукт:')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзив'
        verbose_name_plural = 'Отзивы'

