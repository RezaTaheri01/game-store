from django.views.generic import TemplateView

from .models import SiteSetting

# DRF Imports
from django.db.models import Count, Sum
from products.models import Product
from .models import SlideShow, MainSlideShow
from .serializer import SiteSettingSerializer, SlideShowSerializer, MainSlideShowSerializer
from rest_framework.pagination import LimitOffsetPagination, _positive_int
# DRF Generics
from rest_framework import generics


# Create your views here.
class AboutView(TemplateView):
    template_name = 'site_module/about_us.html'

    def get_context_data(self, **kwargs):
        site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
        context = super(AboutView, self).get_context_data()
        context['site_setting'] = site_setting
        return context


class ServicesView(TemplateView):
    template_name = 'site_module/service.html'

    def get_context_data(self, **kwargs):
        site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
        context = super(ServicesView, self).get_context_data()
        context['site_setting'] = site_setting
        return context


# region DRF
class GenericPagination(LimitOffsetPagination):  # to change page size
    default_limit = 6
    max_limit = 20  # for each page

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


class SiteSettingGenericApiView(generics.ListAPIView):
    queryset = SiteSetting.objects.filter(is_main_setting=True)
    serializer_class = SiteSettingSerializer


class MainSlideShowGenericApiView(generics.ListAPIView):
    serializer_class = MainSlideShowSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        product = Product.objects.filter(is_delete=False, is_active=True)
        main_slide_show = MainSlideShow.objects.all().first()  # query
        if main_slide_show is not None:
            site_setting = SiteSetting.objects.filter(
                is_main_setting=True).first()
            how_many = site_setting.slide_show_number
            if main_slide_show.all and product:
                main_slide_show = product.order_by(
                    main_slide_show.order_by)[:how_many]
            else:
                main_slide_show = main_slide_show.show_list.filter(is_active=True, is_delete=False).order_by(
                    main_slide_show.order_by)
        return main_slide_show


class SlideShowGenericApiView(generics.ListAPIView):
    queryset = SlideShow.objects.filter(
        is_delete=False, is_active=True).order_by('-show_order')
    serializer_class = SlideShowSerializer
    pagination_class = GenericPagination


class SlideShowProductsGenericApiView(generics.ListAPIView):
    serializer_class = MainSlideShowSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        product = Product.objects.filter(
            is_delete=False, is_active=True)  # query not fetch now
        products_list = product.prefetch_related(
            "category__parent_category", "category")
        slide_show: SlideShow = SlideShow.objects.filter(
            pk=pk, is_active=True, is_delete=False).first()
        if slide_show:
            if slide_show.order_by == 'most-visit':
                products = products_list.filter(cartdetail__user_cart__is_paid=True).annotate(
                    sell_count=Sum('cartdetail__product_count')).order_by("-sell_count")
            elif slide_show.order_by == 'most-bought':
                products = products_list.annotate(visit_count=Count("productvisit")).exclude(visit_count=0).order_by(
                    "-visit_count")
            elif slide_show.parent_category:
                products = products_list.filter(category__parent_category=slide_show.parent_category).distinct().order_by(
                    slide_show.order_by)
            elif slide_show.category:
                products = products_list.filter(
                    category=slide_show.category).order_by(slide_show.order_by)
            else:
                products = products_list.order_by('-releaseDate')
        else:
            products = products_list.order_by('-releaseDate')

        return products
# endregion
