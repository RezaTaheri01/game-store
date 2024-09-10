from django.db import models

# Create your models here.
from account.models import User
from products.models import Product
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('user'))
    is_paid = models.BooleanField(default=False, verbose_name=_('paid'))
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name=_('payment date'))
    payment_code = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('payment code'))

    def __str__(self):
        if self.user.first_name != '' and self.user.last_name != '':
            return self.user.get_full_name()  # it's pre ready function
        return self.user.username

    def cal_total_price(self):
        total_price = 0

        if self.is_paid:
            for cartDetail in self.cartdetail_set.all():
                total_price += (cartDetail.final_price * cartDetail.product_count)
        else:
            for cartDetail in self.cartdetail_set.all():
                total_price += (cartDetail.product.current_price() * cartDetail.product_count)

        return total_price

    class Meta:
        verbose_name = _('user cart')
        verbose_name_plural = _('users cart')


class CartDetail(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('product'))
    user_cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, verbose_name=_('user_cart'), default=None)
    final_price = models.IntegerField(null=True, blank=True,
                                      verbose_name=_('final price'))  # this field fill after payment
    product_count = models.IntegerField(verbose_name=_('product count'))

    def total_price(self):
        total_price = 0
        if self.user_cart.is_paid:
            total_price = self.final_price * self.product_count
        else:
            total_price = self.product.current_price() * self.product_count
        return total_price

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _('cart product')
        verbose_name_plural = _('carts products')
