from django.contrib import admin
from . import models


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_paid', 'payment_date', 'payment_code']
    list_filter = ['is_paid', 'payment_date']
    readonly_fields = ['payment_code']
    search_fields = ['payment_code']


class CartDetailAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'product_count', 'final_price']
    list_filter = ['user_cart__user__username']  # interesting :)


admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartDetail, CartDetailAdmin)
