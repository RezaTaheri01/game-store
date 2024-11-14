"""
URL configuration for django5_gamestore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# favicon
from django.views.generic import RedirectView

from . import views
from django.conf import settings  # *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('home/', include('home.urls')),
    path('captcha/', include('captcha.urls')),
    # Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # jwt (when access token expired use refresh token to renew both)
    # send token in header Bearer <token>
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # noster jadi NIP-05
    path('.well-known/nostr.json', views.nostr_view, name='nostr_json'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    # create superuser : python manage.py createsuperuser (password not showed)
    path('products/', include('products.urls')),
    path('contact-us/', include('contact.urls')),
    path('home/', include('home.urls')),
    path('accounts/', include('account.urls')),
    path('user/', include('user_panel.urls')),
    path('cart/', include('cart.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('rosetta/', include('rosetta.urls')),  # python .\manage.py makemessages -l fa_IR --ignore venv
    path('', include('site_module.urls')),
    path('', views.reDirect),
    prefix_default_language=False
)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # *
