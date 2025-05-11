# http://127.0.0.1:8000/products/graphql
# /products/api/all/
# /products/api/comments/{id}/
# /products/api/parent-category/{id}/
# /products/api/main-category/{id}/


import graphene
from graphene_django import DjangoObjectType
from .models import Product, ProductComment, ProductCategory, ParentCategory, ParentParentCategory


# region Categories
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


# endregion


# COMMENT TYPE
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


# QUERY
class Query(graphene.ObjectType):
    product = graphene.Field(ProductType, id=graphene.Int(required=True))

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
