from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории:')

    def __str__(self):
        return self.name

    def products_count(self):
        return self.products.count()

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

    def reviews_list(self):
        return [i.text for i in self.reviews.all()]

    def average_stars(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        return round(sum(r.stars for r in reviews) / reviews.count(), 1)


    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


STARS = (
    (i, '⭐' * i) for i in range(1, 6)
)

class Review(models.Model):
    text = models.TextField(verbose_name='Отзыв:')
    stars = models.IntegerField(choices=STARS, default=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Продукт:')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзив'
        verbose_name_plural = 'Отзивы'


