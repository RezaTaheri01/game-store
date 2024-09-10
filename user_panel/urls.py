from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile_page'),
    path('edit-profile/', views.EditProfilePageView.as_view(), name='edit_profile_page'),
    path('reset-password/', views.ResetPasswordPanelView.as_view(), name='change_password_page'),
    path('cart/', views.user_cart, name='cart_page'),
    path('previous-purchases/', views.PreviousPurchasesView.as_view(), name='previous_purchases_page'),
    path('remove-from-cart/', views.user_cart_remove, name='cart_remove'),
    path('cart-update/', views.user_cart_count, name='cart_update'),

    # DRF
    path('api/profile/<int:pk>/', views.ProfileGenericApiView.as_view(), name='profile_api'),
    path('api/create-user/', views.CreateUserGenericApiView.as_view(), name='create_user_api'),
    path('api/current-user/', views.CurrentUserGenericApiView.as_view(), name='current_user_api'),
    path('api/send-activation/', views.SendActivationEmailGenericAPIView.as_view(), name='activation_email_api'),
    path('api/reset-password/', views.SendForgetPasswordEmailGenericAPIView.as_view(), name='forget_password_api'),
]
