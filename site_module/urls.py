from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about_page'),
    path('service/', views.ServicesView.as_view(), name='service_page'),

    # DRF
    path('home/api/settings/', views.SiteSettingGenericApiView.as_view(), name='setting_api'),
    path('home/api/main-slide-show/', views.MainSlideShowGenericApiView.as_view(), name='main_slideshow_api'),
    path('home/api/slide-shows/', views.SlideShowGenericApiView.as_view(), name='slideshows_api'),
    path('home/api/slide-show/<int:pk>/', views.SlideShowProductsGenericApiView.as_view(), name='slideshow_products_api'),

]
