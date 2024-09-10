from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactUsView.as_view(), name='contact_page'),
    path('api/', views.ContactUsGenericApiView.as_view(), name='contact_us_api'),
]
