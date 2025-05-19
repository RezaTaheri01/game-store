from django.urls import path
from . import views

urlpatterns = [
    # region DRF
    path('api/categories/', views.CategoriesListGenericApiView.as_view(),
         name='categories_api'),
    path('api/category/<int:pk>/', views.CategoryProductsListGenericApiView.as_view(),
         name='category_products_api'),
    path('api/parent-category/<int:pk>/', views.ParentCategoryProductsListGenericApiView.as_view(),
         name='parent_category_products_api'),
    path('api/main-category/<int:pk>/', views.MainCategoryProductsListGenericApiView.as_view(),
         name='main_category_products_api'),
    path('api/all/', views.ProductsListGenericApiView.as_view(), name='products_api'),
    path('api/<int:pk>/', views.ProductDetailGenericApiView.as_view(),
         name='product_detail_api'),
    path('api/comments/<int:pk>/', views.CommentsListGenericApiView.as_view(),
         name='product_comments_api'),
    path('api/add-comment/', views.AddCommentGenericApiView.as_view(),
         name='add_product_comment_api'),
    path('api/dynamic-search/<str:search>/',
         views.DynamicSearchProductsListGenericApiView.as_view(), name='dynamic_search_api'),
    path('api/search/<str:search>/',
         views.SearchProductsListGenericApiView.as_view(), name='search_api'),
    path('api/all-categories/', views.AllCategoriesListGenericApiView.as_view(),
         name='all_categories_api'),
    # endregion

    path('add-comment/', views.addProductComment, name='add-comment'),
    path('search-products/', views.searchProducts, name='search-product'),
    path('search/<str:search>/<slug:farsi>',
         views.ProductSearchView.as_view(), name='search_product_view'),
    path('<slug:slug>/', views.ProductView.as_view(), name='product_page'),
    path('<slug:base>/<slug:slug>/',
         views.ProductListView.as_view(), name='products_page'),
]

# path('order-by/<slug:slug>/', views.ProductListView.as_view(), name='products_page'),
# path('category/<slug:slug>/', views.CategoryFilterView.as_view(), name='category_filter_page'),
# path('parent-category/<slug:slug>/', views.ParentCategoryListView.as_view(), name='parent_category'),
# path('slide-category/<slug:slug>/', views.SlideView.as_view(), name='slide_category_page'),
