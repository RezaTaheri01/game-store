from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model  # get data from auth_user
# Create your views here.
from django.urls import reverse
from django.views import View
from .models import User
from django.utils.crypto import get_random_string
from django.http import Http404, HttpRequest
from account.forms import RegisterForm, SignInForm, ForgetPasswordForm, ResetPasswordForm, ActivationForm
from site_module.models import SiteSetting

# set cookie when log in
from django.contrib.auth import login, logout
from utils.email_service import send_email
from django.utils.translation import gettext_lazy as _


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        register_form = RegisterForm()
        context = {
            'forms': register_form,
            'title': _('Register'),
            'button_title': _('Register'),
            'agree': True,
            'action': reverse('register_page'),
        }
        return render(request, 'account/account.html', context)

    # def form_valid(self, form):
    #     return redirect('home-page')

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('username')
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            profile_image = SiteSetting.objects.filter(is_main_setting=True).first().user_img
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            username: bool = User.objects.filter(username__iexact=user_name).exists()
            if user:
                register_form.add_error('email', _('email repetitive'))
            elif username:
                register_form.add_error('username', _('username repetitive'))
            else:
                # context = str(get_random_string(72))
                # reverse('activate_account', kwargs={'email_active_code': context})
                new_user = User(email=user_email,
                                email_active_code=get_random_string(72),
                                is_active=False,
                                username=user_name,
                                profile_image=profile_image)
                new_user.set_password(user_password)  # for security (inside AbstractUser)
                new_user.save()
                send_email(_('Active Account'), new_user.email, context={'user': new_user,
                                                                         'site_domain': SiteSetting.objects.get(
                                                                             is_main_setting=True).site_url},
                           template_name='email/activate_account.html')
                return redirect('sign_in_page')
        context = {
            'forms': register_form,
            'title': _('Register'),
            'button_title': _('Register'),
            'agree': True,
            'action': reverse('register_page'),
        }
        return render(request, 'account/account.html', context)


class SignInView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
        sign_in_form = SignInForm()
        context = {
            'forms': sign_in_form,
            'title': _('Sign In'),
            'forget_password': True,
            'button_title': _('Sign In'),
            'action': reverse('sign_in_page'),
        }
        return render(request, 'account/account.html', context)

    # def form_valid(self, form):
    #     return redirect('home-page')

    def post(self, request: HttpRequest):  # for intellisense define the variable kind
        if request.user.is_authenticated:
            logout(request)
        sign_in_form = SignInForm(request.POST)
        if sign_in_form.is_valid():
            user_name = sign_in_form.cleaned_data.get('username')
            user_password = sign_in_form.cleaned_data.get('password')

            user: User = User.objects.filter(username__iexact=user_name).first()
            if user is None:
                user: User = User.objects.filter(email__iexact=user_name).first()

            if user is not None:
                # first check account activation
                is_password_correct = user.check_password(user_password)  # convert to hash auto :)
                if is_password_correct:
                    if user.is_active:
                        login(request, user)  # that's it :)
                        # request.session['sign_in'] = True  # create sign in session
                        return redirect(reverse('home-page'))
                        # todo : return to profile panel and change profile menu to profile and exit
                        # for log in you need to set cookie/session
                    else:
                        sign_in_form.add_error('username', _('account is not activated'))
                else:
                    sign_in_form.add_error('username', _('username/email/password incorrect'))
            else:
                sign_in_form.add_error('username', _('username/email/password incorrect'))
        context = {
            'forms': sign_in_form,
            'title': _('Sign In'),
            'forget_password': True,
            'button_title': _('Sign In'),
            'action': reverse('sign_in_page'),
        }
        return render(request, 'account/account.html', context)


class SendActivationEmail(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
        activation_form = ActivationForm()
        context = {
            'forms': activation_form,
            'title': _('Account Activation'),
            'forget_password': False,
            'button_title': _('Submit'),
            'action': reverse('active_account_page'),
        }
        return render(request, 'account/account.html', context)

    def post(self, request: HttpRequest):  # for intellisense define the variable kind
        if request.user.is_authenticated:
            logout(request)
        activation_form = ActivationForm(request.POST)
        if activation_form.is_valid():
            email = activation_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=email, is_active=False).first()

            if user is not None:
                send_email(_('Active Account'), email,
                           context={'user': user,
                                    'site_domain': SiteSetting.objects.get(
                                        is_main_setting=True).site_url},
                           template_name='email/activate_account.html')
                activation_form.add_error('email', _('please check your email'))
            else:
                activation_form.add_error('email', _('already activated or not exist'))
        context = {
            'forms': activation_form,
            'title': _('Account Activation'),
            'forget_password': False,
            'button_title': _('Submit'),
            'action': reverse('active_account_page'),
        }
        return render(request, 'account/account.html', context)


class ActivateView(View):  # work fine
    def get(self, request, email_active_code):
        user = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            logout(request)
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(
                    72)  # after activation change code that no ban user can activate
                # their account by previous code
                user.save()
                # todo : show Success message
                return redirect(reverse('sign_in_page'))
            else:
                # todo : show your account already active message
                # return redirect(reverse('sign_in_page'))
                pass
        else:
            raise Http404
            # todo : show not founded : Done


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm()
        context = {
            'forms': forget_password_form,
            'title': _('Forget Password'),
            'button_title': _('Send'),
            'action': reverse('forget_password_page'),
        }
        return render(request, 'account/account.html', context=context)

    def post(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            email = forget_password_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=email).first()

            if user is not None:
                send_email(_('Reset Password'), user.email, context={'user': user,
                                                                     'site_domain': SiteSetting.objects.get(
                                                                         is_main_setting=True).site_url},
                           template_name='email/reset_password.html')
                forget_password_form.add_error('email', _('reset link send to your email'))
                redirect('home-page')
            else:
                forget_password_form.add_error('email', _('not founded'))
        context = {
            'forms': forget_password_form,
            'title': _('Forget Password'),
            'button_title': _('Send'),
            'action': reverse('forget_password_page'),
        }
        return render(request, 'account/account.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect('sign_in_page')
        else:
            reset_password_form = ResetPasswordForm()
        context = {
            'forms': reset_password_form,
            'title': _('Reset Password'),
            'button_title': _('Send'),
        }
        return render(request, 'account/account.html', context=context)

    def post(self, request: HttpRequest, active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            user: User = User.objects.filter(email_active_code__iexact=active_code).first()
            if user is not None:
                logout(request)  # that's it :)
                new_pass = reset_password_form.cleaned_data.get('password')
                user.set_password(new_pass)
                user.email_active_code = get_random_string(
                    72)
                user.is_active = True
                user.save()
                # request.session['sign_in'] = False  # create sign in session
                return redirect('sign_in_page')
            else:
                reset_password_form.add_error('password', _('not founded'))
        context = {
            'forms': reset_password_form,
            'title': _('Reset Password'),
            'button_title': _('Send'),
        }
        return render(request, 'account/account.html', context)


class SignOutView(View):
    def get(self, request):
        logout(request)
        request.session['sign_in'] = False  # create sign in session
        return redirect('sign_in_page')
