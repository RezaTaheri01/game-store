from rest_framework import serializers
from products.serializer import SimpleProductSerializer
from .models import Cart, CartDetail


class AddCartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        fields = ["id", "product", "product_count"]


class CartDetailSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)

    class Meta:
        model = CartDetail
        fields = ["id", "product", "user_cart", "product_count"]


class CartSerializer(serializers.ModelSerializer):
    cartdetail_set = CartDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = "__all__"


class VerifyCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
