# http://127.0.0.1:8000/cart/graphql
# /user/api/current-user/ # return current user id
# /user/api/profile/{id}/ # profile base on user id
# /cart/api/cart/{id}/ # cart base on user id
# /cart/api/cart/product/{id}/ # each product detail in cart


import graphene
from graphene_django.types import DjangoObjectType
from account.models import User
from .models import Cart, CartDetail
from products.models import Product


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "title", "price")  # Add more if needed


class CartDetailType(DjangoObjectType):
    class Meta:
        model = CartDetail
        # fields = ("id", "product", "final_price", "product_count")

    product = graphene.Field(ProductType)


class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        fields = ("id", "is_paid", "payment_date",
                  "payment_code", "cartdetail_set")

    cartdetail_set = graphene.List(CartDetailType)

    def resolve_cartdetail_set(self, info):
        return self.cartdetail_set.all()


class Query(graphene.ObjectType):
    my_cart = graphene.Field(CartType)
    user = graphene.Field(UserType)

    def resolve_my_cart(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        return Cart.objects.filter(user=user).first()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        return user


schema = graphene.Schema(query=Query)
