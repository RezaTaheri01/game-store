from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from products.models import Product, ProductCategory, ParentCategory, ParentParentCategory, ProductGallery


@login_required
def index(request: HttpRequest):
    return render(request, 'admin_panel/home/index.html')


@login_required
def gallery_add(request: HttpRequest, pk):
    return render(request, 'admin_panel/product_module/product_gallery/add_images.html', context={'pk': pk})


@login_required
def multi_product_gallery(request: HttpRequest):
    if request.method == "POST":
        files = request.FILES.getlist("image")
        key = int(request.POST.get("key"))
        for i in files:
            ProductGallery.objects.create(product_id=key, image=i)
    return redirect(reverse('admin_products'))


# Product
@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    # paginate_by = 12
    template_name = 'admin_panel/product_module/product/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data()
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        # data = Product.objects.filter(category__parent_category__id=1)
        return query


@method_decorator(login_required, name='dispatch')
class ProductChangeView(UpdateView):
    model = Product
    template_name = 'admin_panel/product_module/product/change_product.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_products')
    # success_url = '/admin-panel/product_module'


@method_decorator(login_required, name='dispatch')
class NewProductView(CreateView):
    model = Product
    template_name = 'admin_panel/product_module/product/add_product.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_products')
    # success_url = '/admin-panel/product_module'


@method_decorator(login_required, name='dispatch')
class DeleteProductView(DeleteView):
    template_name = 'admin_panel/confirm/confirm_delete.html'
    model = Product
    success_url = reverse_lazy("admin_products")


# Product Category
@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):
    model = ProductCategory
    # paginate_by = 12
    template_name = 'admin_panel/product_module/category/category_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        return context

    def get_queryset(self):
        query = super(CategoryListView, self).get_queryset()
        return query


@method_decorator(login_required, name='dispatch')
class CategoryChangeView(UpdateView):
    model = ProductCategory
    template_name = 'admin_panel/product_module/category/change_category.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_product_categories')
    # success_url = '/admin-panel/product_module'


@method_decorator(login_required, name='dispatch')
class NewCategoryView(CreateView):
    model = ProductCategory
    template_name = 'admin_panel/product_module/category/add_category.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_product_categories')
    # success_url = '/admin-panel/product_module'


@method_decorator(login_required, name='dispatch')
class DeleteCategoryView(DeleteView):
    template_name = 'admin_panel/confirm/confirm_delete.html'
    model = ProductCategory
    success_url = reverse_lazy("admin_product_categories")


# Parent Category
@method_decorator(login_required, name='dispatch')
class PCategoryListView(ListView):
    model = ParentCategory
    # paginate_by = 12
    template_name = 'admin_panel/product_module/parent_category/p_category_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PCategoryListView, self).get_context_data()
        return context

    def get_queryset(self):
        query = super(PCategoryListView, self).get_queryset()
        return query


@method_decorator(login_required, name='dispatch')
class PCategoryChangeView(UpdateView):
    model = ParentCategory
    template_name = 'admin_panel/product_module/parent_category/change_p_category.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_p_categories')
    # success_url = '/admin-panel/product_module'


@method_decorator(login_required, name='dispatch')
class NewPCategoryView(CreateView):
    model = ParentCategory
    template_name = 'admin_panel/product_module/parent_category/add_p_category.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_p_categories')
    # success_url = '/admin-panel/product_module'


@method_decorator(login_required, name='dispatch')
class DeletePCategoryView(DeleteView):
    template_name = 'admin_panel/confirm/confirm_delete.html'
    model = ParentCategory
    success_url = reverse_lazy("admin_p_categories")


# Grand Parent Category
@method_decorator(login_required, name='dispatch')
class GPCategoryListView(ListView):
    model = ParentParentCategory
    # paginate_by = 12
    template_name = 'admin_panel/product_module/grand_parent_category/gp_category_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(GPCategoryListView, self).get_context_data()
        return context

    def get_queryset(self):
        query = super(GPCategoryListView, self).get_queryset()
        return query


@method_decorator(login_required, name='dispatch')
class GPCategoryChangeView(UpdateView):
    model = ParentParentCategory
    template_name = 'admin_panel/product_module/grand_parent_category/change_gp_category.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_gp_categories')
    # success_url = '/admin-panel/product_module'


@method_decorator(login_required, name='dispatch')
class NewGPCategoryView(CreateView):
    model = ParentParentCategory
    template_name = 'admin_panel/product_module/grand_parent_category/add_gp_category.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_gp_categories')
    # success_url = '/admin-panel/product_module'


@method_decorator(login_required, name='dispatch')
class DeleteGPCategoryView(DeleteView):
    template_name = 'admin_panel/confirm/confirm_delete.html'
    model = ParentParentCategory
    success_url = reverse_lazy("admin_gp_categories")
# --------------------------------------------------
