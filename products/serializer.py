from rest_framework import serializers
from .models import ProductCategory, Product, ProductComment, ParentCategory, ParentParentCategory, ProductGallery


# region Comments
class ProductSubCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['comment', 'product', 'parent', 'user']


class ProductCommentsSerializer(serializers.ModelSerializer):
    sub_comment = ProductSubCommentsSerializer(read_only=True, many=True)

    class Meta:
        model = ProductComment
        fields = ['id', 'comment', 'product', 'user', 'sub_comment']


# endregion

# region All Categories

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title']  # url_title is unique


class ParentCategorySerializer(serializers.ModelSerializer):
    productcategory_set = ProductCategorySerializer(read_only=True, many=True)

    class Meta:
        model = ParentCategory
        fields = ['id', 'title', 'productcategory_set']  # url_title is unique


class ParentParentCategorySerializer(serializers.ModelSerializer):
    parentcategory_set = ParentCategorySerializer(read_only=True, many=True)

    class Meta:
        model = ParentParentCategory
        fields = ['id', 'title', 'parentcategory_set']  # url_title is unique


# endregion

# region Product
class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True, many=True)
    productgallery_set = ProductGallerySerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'image_bg', 'price', 'inventory', 'short_description', 'description',
                  'releaseDate', 'discount', 'category', 'productgallery_set']  # slug is unique


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'price', 'inventory', 'short_description',
                  'releaseDate', 'discount']  # slug is unique


class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'price', 'inventory', 'short_description',
                  'releaseDate', 'discount']  # slug unique

# endregion
