import datetime

from django.contrib import admin
from django.http import HttpRequest

from . import models


# python manage.py createsuperuser
# Register your models here.
# customize in admin panel
class ProductAdmin(admin.ModelAdmin):
    # readonly_fields = ['slug']  # showing slug but readonly
    prepopulated_fields = {  # change slug by entering title at the same time
        'slug': ['title']
    }
    list_display = ['__str__', 'is_active', 'is_delete', 'releaseDate', 'author']
    search_fields = ['title']
    filter_horizontal = ['category', ]
    # raw_id_fields = ('category',) # interesting
    # filter_vertical = ['category']
    # # # filter
    list_filter = ['category__parent_category', 'is_active']  # wow
    # # edit
    list_editable = ['is_active', 'is_delete']

    readonly_fields = ['addDate']

    # add automatically
    def save_model(self, request: HttpRequest, obj: models.Product, form, change):
        if not change:
            obj.author = request.user
            obj.addDate = datetime.date.today()
        return super().save_model(request, obj, form, change)

    # actions = [addDiscount, removeDiscount]


# category
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {  # change slug by entering title at the same time
        'url_title': ['title']
    }
    list_display = ['__str__', 'is_active', 'is_delete']

    # # edit
    list_editable = ['is_active', 'is_delete']

    list_filter = ['parent_category']


class ParentCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {  # change slug by entering title at the same time
        'slug': ['title']
    }
    list_display = ['__str__', 'is_active', 'is_delete']
    # add Product to admin page


class ParentParentCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {  # change slug by entering title at the same time
        'slug': ['title']
    }
    list_display = ['__str__', 'is_active', 'is_delete']
    # add Product to admin page


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'confirm_by_admin']
    list_editable = ['confirm_by_admin']


class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image']
    list_editable = ['image']
    list_filter = ['product']
    raw_id_fields = ('product',)  # interesting


admin.site.register(models.ProductCategory, CategoryAdmin)
admin.site.register(models.ParentCategory, ParentCategoryAdmin)
admin.site.register(models.ParentParentCategory, ParentParentCategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
# admin.site.register(models.ProductTags)
admin.site.register(models.ProductComment, ProductCommentAdmin)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery, ProductGalleryAdmin)
