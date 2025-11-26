from  rest_framework.decorators import  api_view
from  rest_framework.response import Response
from  rest_framework import status
from  .models import Category, Product, Review

from .serializers import CategoryListSerializers, CategoryDetailSerializers, ProductListSerializers, \
    ProductDetailSerializers, ReviewListSerializers, ReviewDetailSerializers

from . import  models

@api_view(http_method_names=['GET'])
def category_list_api_view(request):
    categorys = Category.objects.all()
    data = CategoryListSerializers(categorys, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        categorys = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailSerializers(categorys).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductListSerializers(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        products = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializers(products).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewListSerializers(reviews, many=True).data
    return  Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializers(reviews).data
    return Response(data=data, status=status.HTTP_200_OK)



