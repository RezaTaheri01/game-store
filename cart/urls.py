from django.urls import path
from . import views


# GraphQL
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema


urlpatterns = [
    path('add-to-cart/', views.add_product_to_cart, name='add_to_cart'),
    path('request-payment/', views.request_payment, name='request_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),

    # DRF
    path('api/add-to-cart/', views.AddToCartGenericApiView.as_view(), name='add_to_cart_api'),
    path('api/cart/<int:pk>/', views.CartGenericApiView.as_view(), name='cart_api'),  # get user cart
    path('api/previous-purchase/<int:pk>/', views.PreviousCartGenericApiView.as_view(), name='previous-carts_api'),
    path('api/cart/product/<int:pk>/', views.CartProductGenericApiView.as_view(), name='product_in_cart_api'),

    # GraphQL
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
