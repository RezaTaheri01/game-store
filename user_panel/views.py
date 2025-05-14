from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView
from django.utils.translation import gettext_lazy as _
from django.utils import translation

from account.models import User
from cart.models import CartDetail, Cart
from site_module.models import SiteSetting
from .forms import EditProfileModelForm, ResetPasswordInPanelForm

# DRF Imports
from utils.email_service import send_email_api

from rest_framework.response import Response
from .serializer import UserSerializer, EmailSerializer, UserIDSerializer
# DRF Generics
from rest_framework import generics, status
# DRF Auth
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'user_panel/profile.html'

    def get(self, request, *args, **kwargs):
        context = super(ProfileView, self).get(args, kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class EditProfilePageView(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        # edit_form = EditProfileModelForm(initial={
        #     'first_name': current_user.first_name,
        #     'last_name': current_user.last_name,
        #     'telephone_number': current_user.telephone_number,
        #     'address': current_user.address,
        #     'profile_image': current_user.profile_image,
        # })
        try:
            default_profile = SiteSetting.objects.filter(
                is_main_setting=True).first().user_img
        except:
            default_profile = None

        edit_form = EditProfileModelForm(instance=current_user)
        # if request.user.is_authenticated:
        return render(request, 'user_panel/edit_profile.html', {
            'form': edit_form,
            'user_image': default_profile,
        })
        # raise Http404('User Not Found')

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(
            request.POST, request.FILES, instance=current_user)

        if edit_form.is_valid():
            edit_form.save()
            return redirect('profile_page')
        else:
            try:
                default_profile = SiteSetting.objects.filter(
                    is_main_setting=True).first().user_img
            except:
                default_profile = None
            context = {
                'form': edit_form,
                'user_image': default_profile,
            }

        return render(request, 'user_panel/edit_profile.html', context)


@method_decorator(login_required, name='dispatch')
class ResetPasswordPanelView(View):
    def get(self, request: HttpRequest):
        user: User = User.objects.filter(id=request.user.id).first()
        if user is None:
            return redirect('sign_in_page')
        else:
            reset_password_form = ResetPasswordInPanelForm()
        context = {
            'forms': reset_password_form,
            'title': _('Reset Password'),
            'button_title': _('Send'),
        }
        # if request.user.is_authenticated:
        return render(request, 'account/account.html', context=context)
        # raise Http404('User Not Found')

    def post(self, request: HttpRequest):
        reset_password_form = ResetPasswordInPanelForm(request.POST)
        if reset_password_form.is_valid():
            current_user: User = User.objects.filter(
                id=request.user.id).first()
            if current_user is not None:
                if current_user.check_password(reset_password_form.cleaned_data.get('current_password')):
                    logout(request)  # that's it :)
                    new_pass = reset_password_form.cleaned_data.get('password')
                    current_user.set_password(new_pass)
                    current_user.is_active = True
                    current_user.save()
                    # request.session['sign_in'] = False  # create sign in session
                    return redirect('sign_in_page')
                else:
                    reset_password_form.add_error(
                        'current_password', _('current password is wrong!'))
            else:
                reset_password_form.add_error('password', _('not founded'))
        context = {
            'forms': reset_password_form,
            'title': _('Reset Password'),
            'button_title': _('Send'),
        }
        return render(request, 'account/account.html', context)


@login_required
def user_cart(request: HttpRequest):
    userCart, created = Cart.objects.prefetch_related('cartdetail_set').get_or_create(user_id=request.user.id,
                                                                                      is_paid=False)  # get user cart
    # todo : check inventory and count !!!
    for cart_detail in userCart.cartdetail_set.all():
        if cart_detail.product_count > cart_detail.product.inventory:
            cart_detail.delete()

    userCart, created = Cart.objects.prefetch_related('cartdetail_set').get_or_create(user_id=request.user.id,
                                                                                      is_paid=False)  # get user cart
    total_amount = userCart.cal_total_price()
    context = {
        'cart': userCart,
        'sum': total_amount
    }
    return render(request, 'user_panel/cart.html', context=context)


@login_required
def user_cart_remove(request: HttpRequest):
    detail_id = int(request.GET.get('detail_id'))
    current_url = request.GET.get('url') or ''
    if detail_id is None:
        return JsonResponse(dict(status='not found detail id'))

    delete_count, delete_dict = CartDetail.objects.filter(id=detail_id, user_cart__user_id=request.user.id,
                                                          user_cart__is_paid=False).delete()
    if delete_count == 0:
        return JsonResponse(dict(status='not found detail'))

    userCart: Cart = Cart.objects.prefetch_related('cartdetail_set').filter(is_paid=False,
                                                                            user_id=request.user.id).first()
    total_amount = userCart.cal_total_price()
    if '/fa/' in current_url:
        translation.activate('fa')
    context = {
        'cart': userCart,
        'sum': total_amount
    }
    cart_new_body = render_to_string(
        'user_panel/include/product_in_cart.html', context=context)
    translation.deactivate()
    return JsonResponse({
        'status': 'success',
        'body': cart_new_body
    })


@login_required
def user_cart_count(request: HttpRequest):
    product_id = request.GET.get('product_id')
    product_count = request.GET.get('product_count')
    current_url = request.GET.get('url') or ''
    if product_id is None or product_count is None:
        return JsonResponse(dict(status='not found'))

    product: CartDetail = CartDetail.objects.filter(product_id=product_id, user_cart__user_id=request.user.id,
                                                    user_cart__is_paid=False).first()
    if product is None:
        return JsonResponse(dict(status='not found product'))

    product.product_count = product_count
    product.save()

    userCart = Cart.objects.prefetch_related('cartdetail_set').filter(
        is_paid=False, user_id=request.user.id).first()
    total_amount = userCart.cal_total_price()
    if '/fa/' in current_url:
        translation.activate('fa')
    context = {
        'cart': userCart,
        'sum': total_amount
    }
    cart_new_body = render_to_string(
        'user_panel/include/product_in_cart.html', context=context)
    translation.deactivate()
    return JsonResponse({
        'status': 'success',
        'body': cart_new_body
    })


@method_decorator(login_required, name='dispatch')
class PreviousPurchasesView(ListView):
    template_name = 'user_panel/previous_purchases.html'
    model = Cart
    context_object_name = 'user_carts'

    def get_queryset(self):
        query = super(PreviousPurchasesView, self).get_queryset()
        user_carts = query.filter(
            user_id=self.request.user.id, is_paid=True).order_by('-payment_date')
        return user_carts


# region DRF
class CurrentUserGenericApiView(generics.ListAPIView):
    serializer_class = UserIDSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(pk=user_id, is_active=True)


class ProfileGenericApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        curr_user_id = request.user.id
        user_id = self.kwargs.get('pk')
        if curr_user_id != user_id:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Todo : if email change => send activation link to email (Tmp Disable Email) Done
    def update(self, request, *args, **kwargs):
        try:
            curr_user_id = request.user.id
            user_id = self.kwargs.get('pk')
            if curr_user_id != user_id:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            current_user = User.objects.filter(
                pk=user_id, is_active=True).first()
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            try:
                email = data['email']
            except:
                email = None
            if email and User.objects.filter(email=email, is_active=True).exclude(pk=user_id).exists():
                return Response(None, status=status.HTTP_400_BAD_REQUEST)

            self.perform_update(serializer)

            if email and current_user.email != email:
                current_user.is_active = False
                current_user.save()
                send_email_api(_('Active Account'), email,
                               context={'user': current_user,
                                        'site_domain': SiteSetting.objects.get(
                                            is_main_setting=True).site_url},
                               template_name='email/activate_account.html')

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        except:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        curr_user_id = request.user.id
        user_id = self.kwargs.get('pk')
        if curr_user_id != user_id:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateUserGenericApiView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            username = data['username']
            email = data['email']
            if User.objects.filter(email=email, is_active=True).exists():
                return Response(None, status=status.HTTP_400_BAD_REQUEST)

            self.perform_create(serializer)
            new_user = User.objects.filter(username=username).first()
            send_email_api(_('Active Account'), email, context={'user': new_user,
                                                                'site_domain': SiteSetting.objects.get(
                                                                    is_main_setting=True).site_url},
                           template_name='email/activate_account.html')
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class SendActivationEmailGenericAPIView(generics.CreateAPIView):
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            email = data['email']
            user = User.objects.filter(email=email, is_active=False).first()
            if user is not None:
                send_email_api(_('Active Account'), email, context={'user': user,
                                                                    'site_domain': SiteSetting.objects.get(
                                                                        is_main_setting=True).site_url},
                               template_name='email/activate_account.html')
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class SendForgetPasswordEmailGenericAPIView(generics.CreateAPIView):
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            email = data['email']
            user = User.objects.filter(email=email, is_active=True).first()
            if user is not None:
                send_email_api(_('Reset Password'), user.email, context={'user': user,
                                                                         'site_domain': SiteSetting.objects.get(
                                                                             is_main_setting=True).site_url},
                               template_name='email/reset_password.html')
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
# endregion
