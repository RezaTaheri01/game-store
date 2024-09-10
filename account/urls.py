from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('sign-in/', views.SignInView.as_view(), name='sign_in_page'),
    path('active/', views.SendActivationEmail.as_view(), name='active_account_page'),
    path('sign-out/', views.SignOutView.as_view(), name='sign_out_page'),
    path('forget-password/', views.ForgetPasswordView.as_view(), name='forget_password_page'),
    path('reset-password/<active_code>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('activate/<str:email_active_code>/', views.ActivateView.as_view(), name='activate_account'),
]
