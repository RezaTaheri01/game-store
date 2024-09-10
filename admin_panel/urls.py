from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_dashboard'),
    path('add/gallery/<pk>', views.gallery_add, name='gallery_add'),
    path('add/gallery/', views.multi_product_gallery, name='add_product_gallery'),
    # product
    path('product_module/', views.ProductListView.as_view(), name='admin_products'),
    path('product/change/<pk>', views.ProductChangeView.as_view(), name='admin_change_product'),
    path('product/add/', views.NewProductView.as_view(), name='admin_add_product'),
    path('product/delete/<pk>', views.DeleteProductView.as_view(), name='admin_delete_product'),
    # category
    path('product-category/', views.CategoryListView.as_view(), name='admin_product_categories'),
    path('product-category/change/<pk>', views.CategoryChangeView.as_view(), name='admin_change_product_category'),
    path('product-category/add/', views.NewCategoryView.as_view(), name='admin_add_product_category'),
    path('product-category/delete/<pk>', views.DeleteCategoryView.as_view(), name='admin_delete_category'),
    # parent category
    path('parent-category/', views.PCategoryListView.as_view(), name='admin_p_categories'),
    path('parent-category/change/<pk>', views.PCategoryChangeView.as_view(), name='admin_change_p_category'),
    path('parent-category/add/', views.NewPCategoryView.as_view(), name='admin_add_p_category'),
    path('parent-category/delete/<pk>', views.DeletePCategoryView.as_view(), name='admin_delete_p_category'),
    # grandparent category
    path('g-parent-category/', views.GPCategoryListView.as_view(), name='admin_gp_categories'),
    path('g-parent-category/change/<pk>', views.GPCategoryChangeView.as_view(), name='admin_change_gp_category'),
    path('g-parent-category/add/', views.NewGPCategoryView.as_view(), name='admin_add_gp_category'),
    path('g-parent-category/delete/<pk>', views.DeleteGPCategoryView.as_view(), name='admin_delete_gp_category'),
]
