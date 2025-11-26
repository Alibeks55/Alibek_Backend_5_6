from  rest_framework import  serializers
from  . import  models

class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class CategoryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class ProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

class ProductDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

class ReviewListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'

class ReviewDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'