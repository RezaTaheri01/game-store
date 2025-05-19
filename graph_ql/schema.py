# http://127.0.0.1:8000/graphql
# /user/api/current-user/ # return current user id
# /user/api/profile/{id}/ # profile base on user id
# /cart/api/cart/{id}/ # cart base on user id


import graphene
from graphene_django.types import DjangoObjectType
from account.models import User
from cart.models import Cart, CartDetail
from products.models import Product, ProductComment, ProductCategory, ParentCategory, ParentParentCategory


# region Product
class ProductParentParentCategoryType(DjangoObjectType):
    class Meta:
        model = ParentParentCategory


class ProductParentCategoryType(DjangoObjectType):
    parent_parent_category = graphene.List(
        lambda: ProductParentParentCategoryType)

    class Meta:
        model = ParentCategory

    def resolve_parent_parent_category(self, info):
        return self.parent_parent_category.filter(is_delete=False, is_active=True)


class ProductCategoryType(DjangoObjectType):
    parent_category = graphene.List(lambda: ProductParentCategoryType)

    class Meta:
        model = ProductCategory

    def resolve_parent_category(self, info):
        return self.parent_category.filter(is_delete=False, is_active=True)



class ProductCommentType(DjangoObjectType):
    sub_comments = graphene.List(
        lambda: ProductCommentType)  # 👈 recursive definition

    class Meta:
        model = ProductComment

    def resolve_sub_comments(self, info):
        return self.sub_comment.filter(confirm_by_admin=True)


# PRODUCT TYPE
class ProductType(DjangoObjectType):
    comments = graphene.List(ProductCommentType)
    category = graphene.List(ProductCategoryType)

    class Meta:
        model = Product

    def resolve_comments(self, info):
        # you can use relative names instead of productcomment_set
        return self.productcomment_set.filter(parent=None, confirm_by_admin=True)

    def resolve_category(self, info):
        return self.category.filter(is_delete=False, is_active=True)

# endregion


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class ProductTypeCart(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "title", "price")  # Add more if needed


class CartDetailType(DjangoObjectType):
    class Meta:
        model = CartDetail
        # fields = ("id", "product", "final_price", "product_count")

    product = graphene.Field(ProductTypeCart)


class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        fields = ("id", "is_paid", "payment_date",
                  "payment_code", "cartdetail_set", "user")

    cartdetail_set = graphene.List(CartDetailType)

    def resolve_cartdetail_set(self, info):
        return self.cartdetail_set.all()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    my_cart = graphene.Field(CartType)
    product = graphene.Field(ProductType, id=graphene.Int(required=True))

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
    
    def resolve_product(self, info, id):
        return Product.objects.get(pk=id)


schema = graphene.Schema(query=Query)


# {
#   product(id: 1) {
#     title
#     releaseDate
#     shortDescription
#     price
#     image

#     comments {
#       comment
#       subComment{
#         id
#         comment
#       }
#     }

# 		category {
#       title
#       parentCategory {
#         title
#       }
#     }
#   }
# }


# | GraphQL Data | Equivalent REST Endpoints |
# | ------------ | ------------------------- |
# | `myCart`     | 1–2 endpoints             |
# | `me`         | 1 endpoint                |
# | `product`    | 2–4 endpoints             |

# Total Estimated REST Endpoints: 4 to 7
