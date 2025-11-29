from  rest_framework import  serializers
from  . import  models
from .models import Product, Review


class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'products_count']


class CategoryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'



class ProductListSerializers(serializers.ModelSerializer):
    category =serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = '__all__'


class ProductDetailSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = '__all__'



class ReviewListSerializers(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = models.Review
        fields = '__all__'

class ReviewDetailSerializers(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = models.Review
        fields = '__all__'



class ProductReviewListSerializers(serializers.ModelSerializer):
    reviews = ReviewListSerializers(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'reviews', 'average_stars']