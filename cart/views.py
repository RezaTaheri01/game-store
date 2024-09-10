import json
import datetime

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from products.models import Product
from site_module.models import SiteSetting
from .models import Cart, CartDetail

# DRF Imports
from rest_framework.response import Response
from .serializer import CartSerializer, CartDetailSerializer, AddCartDetailSerializer, VerifyCartSerializer
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, _positive_int  # offset
# DRF Generics
from rest_framework import generics, status
# DRF Auth
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


def add_product_to_cart(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    product_count = int(request.GET.get('product_count'))
    if product_count < 1:
        return JsonResponse(dict(status='not valid', message=_('Count not valid :('), icon='error'))
    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True,
                                         is_delete=False).first()  # check product salable
        if product is not None:
            # create or get Cart
            user_cart, created = Cart.objects.get_or_create(user_id=request.user.id,
                                                            is_paid=False)  # get user cart
            # -------------------
            # check if product exist in cart
            current_product = user_cart.cartdetail_set.filter(
                product_id=product_id).first()
            if current_product is not None:
                # todo : check inventory then add
                inventory = product.inventory
                current_in_cart = current_product.product_count
                if current_in_cart + product_count > inventory:
                    return JsonResponse(
                        dict(status='not enough', message=_('Not enough Product :('), icon='error'))
                else:
                    current_product.product_count += product_count
                    current_product.save()
            # create new CartDetail
            else:
                product_to_cart = CartDetail(product_id=product_id, user_cart_id=user_cart.id,
                                             product_count=product_count)
                product_to_cart.save()
            # ----------------------
            return JsonResponse(dict(status='success', message=_('Product successfully added :)'), icon='success', ))
        else:
            return JsonResponse(dict(status='not found', message=_('Product not found :('), icon='error'))
    else:
        return JsonResponse(dict(status='not authenticated', message=_('Please sign in first'), icon='error'))


MERCHANT = settings.MERCHANT
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_START_PAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 10000  # Rial / Required
description = "Payment"  # Required
email = 'GameStorePersia@gmail.com'  # Optional
mobile = ''  # Optional
# . todo : Important: need to edit for deployment
site_domainsite_domain = ''
site_domain = 'http://reza-taheri.ir'
# CallbackURL = site_domain + '/fa/cart/verify-payment/'
# CallbackURL = 'http://reza-taheri.ir/fa/cart/verify-payment/'


@login_required
def request_payment(request: HttpRequest):
    site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
    if site_setting:
        site_domain = site_setting.site_url
    CallbackURL = site_domain + '/fa/cart/verify-payment/'
    current_cart, created = Cart.objects.get_or_create(
        is_paid=False, user_id=request.user.id)
    total_price = current_cart.cal_total_price()
    if total_price == 0:
        return redirect(reverse('cart_page'))

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        # this is a different
        return redirect(ZP_API_START_PAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def add_final_price(current_cart: Cart):
    # todo : I think it can be better
    for product in current_cart.cartdetail_set.all():
        product.final_price = product.product.price
        product.product.inventory = product.product.inventory - product.product_count
        product.save()
        product.product.save()


@login_required
def verify_payment(request: HttpRequest):
    current_cart, created = Cart.objects.prefetch_related('cartdetail_set').get_or_create(is_paid=False,
                                                                                          user_id=request.user.id)
    total_price = current_cart.cal_total_price()
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(
            req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                ref_str = req.json()['data']['ref_id']
                current_cart.is_paid = True
                current_cart.payment_date = datetime.datetime.now()
                current_cart.payment_code = ref_str
                current_cart.save()
                add_final_price(current_cart)

                return render(request, 'user_panel/payment_result.html', {
                    'success': str(ref_str)
                })
            elif t_status == 101:
                return render(request, 'user_panel/payment_result.html', {
                    'info': _('this payment already done (Repetitive)')
                })
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request, 'user_panel/payment_result.html', {
                    'error': str(req.json()['data']['message'])
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return render(request, 'user_panel/payment_result.html', {
                'error': e_message
            })
    else:
        return render(request, 'user_panel/payment_result.html', {
            'error': _('sth went wrong / user cancel payment')
        })


# region DRF
# Pagination
class GenericPagination(LimitOffsetPagination):  # to change page size
    default_limit = 4
    max_limit = 12  # for each page

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                return _positive_int(
                    request.query_params[self.limit_query_param],
                    strict=True,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError) as e:
                raise e  # Re-raise the caught exception

        return self.default_limit


class AddToCartGenericApiView(generics.CreateAPIView):
    serializer_class = AddCartDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            product_id = data['product'].id
            product_count = data['product_count']
            if product_count <= 0:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            user_cart, created = Cart.objects.get_or_create(user_id=request.user.id,
                                                            is_paid=False)  # get user cart
            product_in_cart = CartDetail.objects.filter(
                user_cart_id=user_cart.id, product_id=product_id).first()
            if product_in_cart:
                inv = product_in_cart.product.inventory
                if product_in_cart.product_count + product_count <= inv:
                    product_in_cart.product_count += product_count
                else:
                    return Response(None, status=status.HTTP_406_NOT_ACCEPTABLE)
                cart_product = product_in_cart
            else:
                cart_product: CartDetail = CartDetail(user_cart_id=user_cart.id, product_id=product_id,
                                                      product_count=product_count)
                if cart_product.product.inventory < product_count:
                    return Response(None, status=status.HTTP_406_NOT_ACCEPTABLE)
            cart_product.save()
            serializer = AddCartDetailSerializer(instance=cart_product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class CartGenericApiView(generics.ListAPIView):
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(is_paid=False, user_id=self.kwargs.get('pk'))

    def list(self, request, *args, **kwargs):
        curr_user_id = self.kwargs.get('pk')
        user_id = self.request.user.id
        if curr_user_id != user_id:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PreviousCartGenericApiView(generics.ListAPIView):
    serializer_class = CartSerializer
    pagination_class = GenericPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(is_paid=True, user_id=self.kwargs.get('pk')).order_by('-payment_date')

    def list(self, request, *args, **kwargs):
        curr_user_id = self.kwargs.get('pk')
        user_id = self.request.user.id
        if curr_user_id != user_id:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CartProductGenericApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartDetailSerializer
    queryset = CartDetail.objects.filter(user_cart__is_paid=False)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        product_in_cart_id = self.kwargs.get('pk')
        user_id = request.user.id
        cart_detail_tmp: CartDetail = CartDetail.objects.filter(
            id=product_in_cart_id).first()
        if cart_detail_tmp.user_cart.user_id != user_id or cart_detail_tmp.user_cart.is_paid:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        product_in_cart_id = self.kwargs.get('pk')
        user_id = request.user.id
        cart_detail_tmp: CartDetail = CartDetail.objects.filter(
            id=product_in_cart_id).first()
        if cart_detail_tmp.user_cart.user_id != user_id:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        try:
            product_in_cart_id = self.kwargs.get('pk')
            user_id = request.user.id
            cart_detail_tmp: CartDetail = CartDetail.objects.filter(
                id=product_in_cart_id).first()
            if cart_detail_tmp.user_cart.user_id != user_id:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)

            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            user_cart_id = data['user_cart'].id
            if user_cart_id != cart_detail_tmp.user_cart.id:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)

            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        except:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

# endregion
