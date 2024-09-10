import random
from urllib.parse import unquote

from django.db.models import Count, Q, Sum
from django.http import HttpRequest, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext_lazy as _

from products.models import Product, ProductComment, ProductVisit, ProductGallery
from site_module.models import SlideShow
from utils.http_service import get_client_ip

# DRF Imports
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, _positive_int  # offset
from .serializer import ProductCategorySerializer, ProductSerializer, ProductCommentsSerializer, \
    ProductSubCommentsSerializer, ProductSearchSerializer, ParentParentCategorySerializer, SimpleProductSerializer
# DRF Generics
from rest_framework import generics, status
from products.models import ProductCategory, ParentParentCategory
# DRF Auth
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

search_result_count = 15
card_in_page = 1
order_dict = {
    'price': 'price',
    'releaseDate': 'releaseDate',
    'discount': 'discount',
    'قیمت': 'price',
    'تاریخ عرضه': 'releaseDate',
    'تخفیف': 'discount',
}


# Create your views here.
# show list scenario
class ProductListView(ListView):
    template_name = 'product_module/products.html'
    model = Product  # instead of get_context function
    context_object_name = 'products'  # change name to the same name in filter category class to use both :)
    allow_empty = False
    # paging :)
    paginate_by = card_in_page  # products/?page=<page-number> Structure

    # default name is object_list
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        base = self.kwargs.get('base')
        base_query = super(ProductListView, self).get_queryset()
        base_query = base_query.filter(is_active=True, is_delete=False)
        if base == 'all':
            data = base_query.order_by("-releaseDate")
        elif base == 'parent-category':
            data = base_query.filter(category__parent_category__slug=slug).distinct().order_by('-releaseDate')
        elif base == 'main-category':
            data = base_query.filter(category__parent_category__parent_parent_category__slug=slug).distinct().order_by(
                '-releaseDate')
        elif base == 'slide-category':
            slide = SlideShow.objects.get(id=slug)
            if slide.order_by == 'most-bought':
                data = base_query.filter(cartdetail__user_cart__is_paid=True).annotate(
                    sell_count=Sum("cartdetail__product_count")).order_by("-sell_count")

            elif slide.order_by == 'most-visit':
                data = base_query.annotate(visit_count=Count("productvisit")).exclude(
                    visit_count=0).order_by(
                    "-visit_count")
            else:
                parent = slide.parent_category
                if parent is not None:
                    data = base_query.filter(category__parent_category__slug=parent.slug).distinct().order_by(
                        slide.order_by)
                else:
                    try:
                        cat = slide.category.id
                    except:
                        cat = None
                    if cat is None:
                        data = base_query.order_by(slide.order_by)
                    else:
                        data = base_query.filter(category=cat, category__is_active=True,
                                                 category__is_delete=False).order_by(slide.order_by)
        else:
            data = base_query.filter(category__url_title=slug).order_by('-releaseDate')

        if data.count() != 0:
            start_price = self.request.GET.get('start_price')
            end_price = self.request.GET.get('end_price')
            order = self.request.GET.get('order_by')
            if start_price:
                data = data.filter(price__gte=start_price)
            if end_price:
                data = data.filter(price__lte=end_price)
            if order:
                order_convert = '-' + order_dict.get(str(order))
                data = data.order_by(order_convert)
            return data
        else:
            raise Http404('Not Found')

    def get_context_data(self, *, object_list=None, **kwargs):
        slug = self.kwargs.get('slug')
        base = self.kwargs.get('base')
        # request: HttpRequest = self.request
        context = super().get_context_data(**kwargs)
        if base == 'all':
            context['title'] = _('Products')
        elif base == 'slide-category':
            slide = SlideShow.objects.get(id=slug)
            context['title'] = slide.title
        else:
            context['title'] = str(slug).replace('-', ' ')
        # price field
        max_price = Product.objects.all().order_by("-price").first().price
        start_price = self.request.GET.get('start_price') or 0
        end_price = self.request.GET.get('end_price') or max_price
        if base == 'slide-category':
            # todo : get slideshow order field and send it as order
            order = self.request.GET.get('order_by')
        else:
            order = self.request.GET.get('order_by') or 'releaseDate'
        context['start_price'] = int(start_price)
        context['end_price'] = int(end_price)
        context['max_price'] = int(max_price)
        context['min_price'] = 0
        context['order'] = order
        context['filter_bar'] = True
        # end price field
        return context


class ProductView(DetailView):
    model = Product  # automatically know that which data was requested by slug:slug Wow
    template_name = 'product_module/product_page.html'

    def get_queryset(self):
        query = super(ProductView, self).get_queryset()
        query = query.filter(is_active=True, is_delete=False)
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductView, self).get_context_data()
        product: Product = kwargs.get('object')  # current product
        cat = product.category.all()
        rand = random.randint(0, cat.count() - 1)
        product_gallery: ProductGallery = ProductGallery.objects.filter(product_id=product.id)
        context['product_gallery'] = product_gallery
        correlate_product = Product.objects.filter(category=cat[rand]).exclude(id=product.id).order_by(
            '-releaseDate')[:8]
        context['related_products'] = correlate_product
        comments = ProductComment.objects.filter(product_id=product.id, confirm_by_admin=True,
                                                 parent=None).prefetch_related('sub_comment')

        comments_count = ProductComment.objects.filter(product_id=product.id, confirm_by_admin=True).count()
        # fetch all data you need in one query (performance...)
        context['comments'] = comments.order_by('-create_date')
        context['comments_count'] = comments_count
        # Get ip for visit
        request: HttpRequest = self.request
        user_id = None
        user_ip = get_client_ip(request)
        # if request.user.is_authenticated:
        #     user_id = request.user.id
        try:

            if request.user.is_authenticated:
                user_id = request.user.id
                has_been_visit = ProductVisit.objects.filter(product_id=product.id, user=user_id).exists()

            else:
                has_been_visit = ProductVisit.objects.filter(product_id=product.id, ip__iexact=user_ip).exists()

            if not has_been_visit:
                new_visit = ProductVisit(user=user_id, ip=user_ip, product_id=product.id)
                new_visit.save()
        except:
            pass
        # ----------------
        # print(kwargs)  # value is current product
        return context


def addProductComment(request: HttpRequest):
    if request.user.is_authenticated:
        product_id = request.GET.get("product_id")
        parent_id = request.GET.get("parent_id")
        if parent_id == '':
            parent_id = None
        comment = request.GET.get("product_comment")
        # print(product_id, comment)
        if comment != '':
            new_comment = ProductComment(product_id=product_id, parent_id=parent_id, user_id=request.user.id,
                                         comment=comment)
            new_comment.save()
        comment = ProductComment.objects.filter(product_id=product_id, confirm_by_admin=True)
        context = {
            "comments": comment.filter(parent=None, confirm_by_admin=True).order_by("-create_date").prefetch_related(
                'sub_comment'),
            "comments_count": comment.count(),
            "product_id": product_id,

        }
        # Context = render_to_string(request=request, template_name='product_module/include/product_comment_partial.html',
        #                            context=context)
        # return JsonResponse({
        #     'body': Context,
        #     "icon": 'info',
        #     'message': _('visible after admin confirmation')
        # })
        return render(request, 'product_module/include/product_comment_partial.html', context=context)  # send to js


def searchProducts(request: HttpRequest):
    search_text = request.GET.get('search')
    dynamic = int(request.GET.get('dynamic') or 0)
    url = request.GET.get('url') or ''
    products = None

    if search_text != '' and search_text != ' ' and search_text != '  ':
        products = Product.objects.filter(is_active=True, is_delete=False)
    if dynamic == 1:
        products = products.filter(
            Q(title__icontains=search_text) | Q(title_fa__icontains=search_text) | Q(
                title_en__icontains=search_text) | Q(
                slug__icontains=search_text)).order_by(
            '-releaseDate').distinct()[:search_result_count]  # 15
        return JsonResponse({
            'status': 'success',
            'body': render_to_string(request=request, template_name='include/header/dynamic_search_result.html',
                                     context={'products': products})
        })
    else:
        if products:
            farsi = 'En'
            if '/fa/' in url:
                farsi = 'Fa'
            reDirect_link = reverse('search_product_view', args=[search_text, farsi])
            return HttpResponseRedirect(reDirect_link)
        else:
            raise Http404('not found')
        # if products:
        #     farsi = False
        #     if '/fa/' in url:
        #         farsi = True
        #     products = products.filter(Q(title__icontains=search_text) | Q(title_fa__icontains=search_text) | Q(
        #         title_en__icontains=search_text) | Q(slug__icontains=search_text)).order_by(
        #         '-releaseDate').distinct()[:search_result_count]
        #     return render(request, 'product_module/products.html', context={
        #         'products': products,
        #         'title': search_text,
        #         'filter_bar': False,
        #         'farsi': farsi,
        #     })
        # else:
        #     raise Http404('not found')


class ProductSearchView(ListView):
    template_name = 'product_module/products.html'
    model = Product  # instead of get_context function
    context_object_name = 'products'  # change name to the same name in filter category class to use both :)
    allow_empty = False
    # paging :)
    paginate_by = card_in_page  # products/?page=<page-number> Structure

    # default name is object_list
    def get_queryset(self):
        search_text = self.kwargs.get('search')
        search_text = unquote(search_text)
        products = super(ProductSearchView, self).get_queryset()
        products = products.filter(is_active=True, is_delete=False)
        products = products.filter(Q(title__icontains=search_text) | Q(title_fa__icontains=search_text) | Q(
            title_en__icontains=search_text) | Q(slug__icontains=search_text)).order_by(
            '-releaseDate').distinct()
        products = products.order_by("-releaseDate")
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        search_text = self.kwargs.get('search')
        farsi = self.kwargs.get('farsi')
        search_text = unquote(search_text)

        context = super().get_context_data(**kwargs)
        context['title'] = search_text
        context['filter_bar'] = False
        if farsi == 'Fa':
            context['farsi'] = True
        else:
            context['farsi'] = False

        return context


# class ParentCategoryListView(ListView):
#     template_name = 'product_module/products.html'
#     model = Product  # instead of get_context function
#     context_object_name = 'products'  # change name to the same name in filter category class to use both :)
#     allow_empty = False
#     # paging :)
#     paginate_by = 6  # products/?page=<page-number> Structure
#
#     # default name is object_list
#     def get_queryset(self):
#         slug = self.kwargs.get('slug')
#         base_query = super(ParentCategoryListView, self).get_queryset()
#         data = base_query.filter(category__parent_category__slug=slug).distinct().order_by('-releaseDate')
#         if data.count() != 0:
#             return data
#         else:
#             raise Http404("no product found")
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         slug = self.kwargs.get('slug')
#         context = super().get_context_data(**kwargs)
#         context['title'] = str(slug).replace('-', ' ')
#         return context
# ---------------------------------------------------------------------
# class CategoryFilterView(ListView):
#     template_name = 'product_module/products.html'
#     model = Product
#     context_object_name = 'products'
#     allow_empty = False
#     paginate_by = 6  # todo : find a better way !
#
#     def get_queryset(self):
#         slug = self.kwargs.get('slug')
#         base_query = super(CategoryFilterView, self).get_queryset()
#         data = base_query.filter(is_active=True, is_delete=False,
#                                  category__url_title=slug).order_by('-releaseDate')
#         return data
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         slug = self.kwargs.get('slug')
#         context = super(CategoryFilterView, self).get_context_data()
#         context['title'] = str(slug).replace('-', ' ')
#         return context
# ------------------------------------------------------------
# class SlideView(TemplateView):
#     template_name = 'product_module/products.html'
#
#     def get_context_data(self, **kwargs):
#         slug = self.kwargs.get('slug')
#         context = super(SlideView, self).get_context_data()
#         slide = SlideShow.objects.get(id=slug)
#         cat = slide.category
#         products = Product.objects.filter(is_delete=False, is_active=True)
#         if slide.category is None:
#             products = products.order_by(slide.order_by)
#         else:
#             products = products.filter(category__title=cat, category__is_active=True,
#                                        category__is_delete=False).order_by(slide.order_by)
#         if products is not None:
#             context['title'] = slide.title
#             context['products'] = products
#         return context

# region DRF
# Pagination
class GenericPagination(LimitOffsetPagination):  # to change page size
    default_limit = 1
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


class CategoriesListGenericApiView(generics.ListAPIView):
    queryset = ProductCategory.objects.filter(is_active=True, is_delete=False)
    serializer_class = ProductCategorySerializer
    pagination_class = GenericPagination


class CategoryProductsListGenericApiView(generics.ListAPIView):
    serializer_class = SimpleProductSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        pk = self.kwargs['pk']
        products = Product.objects.filter(is_active=True, is_delete=False, category=pk)
        orderBy = self.request.query_params.get('order_by') or '-releaseDate'
        try:
            products = products.order_by(orderBy)
        except:
            products = products.order_by('-releaseDate')
        return products


class ParentCategoryProductsListGenericApiView(generics.ListAPIView):
    serializer_class = SimpleProductSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        pk = self.kwargs['pk']
        products = Product.objects.filter(is_active=True, is_delete=False, category__parent_category=pk).distinct()
        orderBy = self.request.query_params.get('order_by') or '-releaseDate'
        try:
            products = products.order_by(orderBy)
        except:
            products = products.order_by('-releaseDate')
        return products


class MainCategoryProductsListGenericApiView(generics.ListAPIView):
    serializer_class = SimpleProductSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        pk = self.kwargs['pk']
        products = Product.objects.filter(is_active=True, is_delete=False,
                                          category__parent_category__parent_parent_category=pk).distinct()
        orderBy = self.request.query_params.get('order_by') or '-releaseDate'
        try:
            products = products.order_by(orderBy)
        except:
            products = products.order_by('-releaseDate')
        return products


class ProductsListGenericApiView(generics.ListAPIView):
    serializer_class = SimpleProductSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        orderBy = self.request.query_params.get('order_by') or '-releaseDate'
        try:
            products = Product.objects.filter(is_active=True, is_delete=False).order_by(orderBy)
        except:
            products = Product.objects.filter(is_active=True, is_delete=False).order_by('-releaseDate')
        return products


class ProductDetailGenericApiView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CommentsListGenericApiView(generics.ListAPIView):
    serializer_class = ProductCommentsSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        orderBy = self.request.query_params.get('order_by') or '-create_date'
        comments = ProductComment.objects.filter(product_id=pk, parent=None, confirm_by_admin=True)
        try:
            product_comments = comments.order_by(orderBy)
        except:
            product_comments = comments.order_by("-create_date")
        return product_comments  # get parents


# Todo: Check If Comment is Empty or None
class AddCommentGenericApiView(generics.CreateAPIView):
    serializer_class = ProductSubCommentsSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            current_user_id = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            user = data['user']
            if user is None:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            if user.id != current_user_id:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)

            parent_product = data['parent']
            product_id = data['product'].id
            if parent_product and parent_product.product.id != product_id:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class DynamicSearchProductsListGenericApiView(generics.ListAPIView):
    serializer_class = ProductSearchSerializer

    def get_queryset(self):
        search_text = self.kwargs.get('search')
        search_text = unquote(search_text)
        products = None

        if search_text != '' and search_text != ' ' and search_text != '  ':
            products = Product.objects.filter(is_active=True, is_delete=False)
            products = products.filter(
                Q(title__icontains=search_text) | Q(title_fa__icontains=search_text) | Q(
                    title_en__icontains=search_text) | Q(
                    slug__icontains=search_text)).order_by(
                '-releaseDate').distinct()[:search_result_count]  # 15

        return products


class SearchProductsListGenericApiView(generics.ListAPIView):
    serializer_class = ProductSearchSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        search_text = self.kwargs.get('search')
        search_text = unquote(search_text)
        products = None

        if search_text != '' and search_text != ' ' and search_text != '  ':
            orderBy = self.request.query_params.get('order_by') or '-releaseDate'
            products = Product.objects.filter(is_active=True, is_delete=False)
            products = products.filter(
                Q(title__icontains=search_text) | Q(title_fa__icontains=search_text) | Q(
                    title_en__icontains=search_text) | Q(
                    slug__icontains=search_text)).distinct()
            try:
                products = products.order_by(orderBy)
            except:
                products = products.order_by('-releaseDate')
        return products


class AllCategoriesListGenericApiView(generics.ListAPIView):
    queryset = ParentParentCategory.objects.filter(is_active=True, is_delete=False)
    serializer_class = ParentParentCategorySerializer
# endregion
