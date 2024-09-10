from django.db.models import Count, Sum
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from products.models import Product
from site_module import models
from site_module.models import SlideShow, MainSlideShow, SiteSetting


# Using TemplateView(better)
class HomeView(TemplateView):
    template_name = 'home/home.html'

    # todo : need improvement !
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        numberList = []
        s_num = 15

        product = Product.objects.filter(is_delete=False, is_active=True)  # query not fetch now

        main_slide_show = MainSlideShow.objects.all().first()  # query
        if main_slide_show is not None:
            site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
            how_many = site_setting.slide_show_number
            # how_many = 8
            if main_slide_show.all and product:
                main_slide_show = product.order_by(main_slide_show.order_by)[:how_many]
            else:
                main_slide_show = main_slide_show.show_list.filter(is_active=True, is_delete=False).order_by(
                    main_slide_show.order_by)

            for i in range(1, main_slide_show.count() + 1):
                numberList.append(i)
            context['products'] = list(main_slide_show)  # in this place fetch data from db

        site_setting = models.SiteSetting.objects.filter(is_main_setting=True).first()  # query
        if site_setting is not None:
            context['title'] = site_setting.site_name
            context['home_img'] = site_setting.home_img

        context['numbers'] = numberList
        context['current_page'] = _('home')

        # ----------------------------------------------------------------
        
        main_list = []

        slides = SlideShow.objects.filter(is_active=True, is_delete=False)  # query

        slide_by_buy = slides.filter(order_by='most-bought').first()
        slide_by_visits = slides.filter(order_by='most-visit').first()
        slide_show = list(slides.filter(parent_category=None).order_by(
            '-show_order'))  # when using list before query it get query instantly
        # if not it wait until you use it.
        slide_show_parent_base = list(slides.exclude(parent_category=None).order_by(
            '-show_order'))
        products_list = product.prefetch_related("category__parent_category", "category")

        counter = 0

        if slide_by_buy:
            items = get_slide(counter, slide_by_buy, product, s_num, -1)
            main_list.append(items)
            counter += 1

        if slide_by_visits:
            items = get_slide(counter, slide_by_visits, product, s_num, 0)
            main_list.append(items)
            counter += 1

        for s in slide_show:
            if s.order_by != 'most-visit' and s.order_by != 'most-bought':
                items = get_slide(counter, s, products_list, s_num, 1)
                main_list.append(items)
                counter += 1

        for s in slide_show_parent_base:
            if s.order_by != 'most-visit' and s.order_by != 'most-bought':
                items = get_slide(counter, s, products_list, s_num, 2)
                main_list.append(items)
                counter += 1
        main_list = Sort(main_list)
        context['slide_show_all'] = list(main_list)
        return context


def get_slide(counter, s, products_list, s_num, which):
    item_by_parent = [s.show_order, {'counter': counter, 'id': s.id, 'title': s.title}]
    if which == -1:
        products = products_list.filter(cartdetail__user_cart__is_paid=True).annotate(
            sell_count=Sum('cartdetail__product_count')).order_by("-sell_count")[:s_num]
    elif which == 0:
        products = products_list.annotate(visit_count=Count("productvisit")).exclude(visit_count=0).order_by(
            "-visit_count")[:s_num]

    elif which == 1:
        products = products_list.filter(category=s.category).order_by(s.order_by)[:s_num]
        if products.count() == 0:
            products = products_list.order_by(s.order_by)[:s_num]

    else:
        products = products_list.filter(category__parent_category=s.parent_category).distinct().order_by(
            s.order_by)[:s_num]

    item_by_parent.append({'products': list(products),
                           'id': s.id})
    item_by_parent.append(counter)
    return item_by_parent


# order main list base on show_order ( code is not mine )
def Sort(sub_li):
    length = len(sub_li)

    for i in range(0, length):
        for j in range(0, length - i - 1):

            if sub_li[j][0] < sub_li[j + 1][0]:
                tempo = sub_li[j]
                sub_li[j] = sub_li[j + 1]
                sub_li[j + 1] = tempo

    return sub_li


def change_language(request: HttpRequest, lg):
    if lg == 'fa':
        settings.LANGUAGE_CODE = 'fa-ir'
    else:
        settings.LANGUAGE_CODE = 'en-us'
    return redirect(reverse('home-page'))


class MemoryView(TemplateView):
    template_name = 'home/include/memory_management.html'


class FirstFollowView(TemplateView):
    template_name = 'home/include/etc/first_follow.html'


class ChainRulesView(TemplateView):
    template_name = 'home/include/etc/chain_rules.html'
# class SlideView(TemplateView):
#     template_name = 'product_module/products.html'
#     allow_empty = False
#     paginate_by = 6
#     models = Product
#
#     def get_context_data(self, **kwargs):
#         context = super(SlideView, self).get_context_data()
#         slug = self.kwargs.get('slug')
#         slide = SlideShow.objects.get(pk=slug)
#         cat = slide.category
#         products = Product.objects.get(category__title=cat)
#         context['title'] = slide.title
#         context['products'] = products
#         return context
# need install package : pip install django-render-partial
# better than include for db usage

# class SessionView(View):
#     def post(self, request):
#         value = request.POST['value']
#         request.session['value'] = value
#         return redirect(reverse('home-page'))
