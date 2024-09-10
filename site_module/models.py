from django.db import models

from products.models import Product, ParentCategory, ProductCategory
from django.utils.translation import gettext_lazy as _

orderByDict = [  # for choice list
    ('releaseDate', 'releaseDate'),
    ('-releaseDate', '-releaseDate'),
    ('addDate', 'addDate'),
    ('-addDate', '-addDate'),
    ('price', 'price'),
    ('-price', '-price'),
    ('discount', 'discount'),
    ('-discount', '-discount'),
    ('title', 'title'),
    ('-title', '-title'),
    ('most-visit', 'most-visit'),
    ('most-bought', 'most-bought'),
]

orderByDictMain = [  # for choice list
    ('releaseDate', 'releaseDate'),
    ('-releaseDate', '-releaseDate'),
    ('addDate', 'addDate'),
    ('-addDate', '-addDate'),
    ('price', 'price'),
    ('-price', '-price'),
    ('discount', 'discount'),
    ('-discount', '-discount'),
    ('title', 'title'),
    ('-title', '-title'),
]


# Create your models here.
class SiteSetting(models.Model):
    is_main_setting = models.BooleanField(default=False, verbose_name=_('main setting'), blank=True)
    site_name = models.CharField(max_length=72, verbose_name=_('site name'))
    site_url = models.CharField(max_length=72, verbose_name=_('site domain'))
    site_logo = models.ImageField(upload_to='images/site_module/', verbose_name=_('site logo'), blank=True)
    site_icon = models.ImageField(upload_to='images/site_module/', verbose_name=_('site icon'), null=True, blank=True)

    slide_show_number = models.IntegerField(default=2, choices=((i, i) for i in range(2, 20)),
                                            verbose_name=_('main slide show number'))
    address = models.TextField(max_length=72, verbose_name=_('address'), blank=True, null=True)
    phone = models.CharField(max_length=72, verbose_name=_('phone number'), blank=True, null=True)
    email = models.CharField(max_length=72, verbose_name=_('email'), blank=True, null=True)
    copy_right = models.TextField(verbose_name=_('copyright'))
    services = models.TextField(verbose_name=_('services'), null=True)
    about_us = models.TextField(verbose_name=_('about us'), blank=True, null=True)
    preload_icon = models.ImageField(upload_to='images/site_module/', verbose_name=_('preload icon'), null=True,
                                     blank=True, db_index=True)
    home_img = models.ImageField(upload_to='images/site_module/', verbose_name=_('home image'), null=True, blank=True)
    user_img = models.ImageField(upload_to='images/site_module/', verbose_name=_('default user profile'), null=True)
    account_img = models.FileField(upload_to='images/site_module/', verbose_name=_('account page image'), null=True,
                                   blank=True)
    contact_img = models.FileField(upload_to='images/site_module/', verbose_name=_('contact us page image'), null=True,
                                   blank=True)

    social_1_icon = models.ImageField(upload_to='images/site_module/', verbose_name=_('social media icon'), null=True,
                                      blank=True)
    social_1 = models.CharField(max_length=144, verbose_name=_('social media above link'), null=True, blank=True)
    social_2_icon = models.ImageField(upload_to='images/site_module/', verbose_name=_('social media icon'), null=True,
                                      blank=True)
    social_2 = models.CharField(max_length=144, verbose_name=_('social media above link'), null=True, blank=True)
    social_3_icon = models.ImageField(upload_to='images/site_module/', verbose_name=_('social media icon'), null=True,
                                      blank=True)
    social_3 = models.CharField(max_length=144, verbose_name=_('social media above link'), null=True, blank=True)
    social_4_icon = models.ImageField(upload_to='images/site_module/', verbose_name=_('social media icon'), null=True,
                                      blank=True)
    social_4 = models.CharField(max_length=144, verbose_name=_('social media above link'), null=True, blank=True)

    class Meta:
        verbose_name = _('site setting')
        verbose_name_plural = _('site settings')

    def __str__(self):
        return self.site_name


class MainSlideShow(models.Model):
    class OrderChoices(models.TextChoices):
        product_list = 'product_list', 'لیست محصولات',
        product_detail = 'product_detail', 'جزِییات محصولات',
        about_us = 'about_us', 'درباره ما',

    show_list = models.ManyToManyField(to=Product, verbose_name=_('products'), blank=True,
                                       related_name='show_list')
    note = models.CharField(default=_('if you choose all products not matter'),
                            max_length=128)
    all = models.BooleanField(default=False, verbose_name=_('choose all products'))
    order_by = models.CharField(default='releaseDate', choices=orderByDictMain, max_length=256,
                                verbose_name=_('order by'))
    choice_field = models.CharField(default='', choices=OrderChoices.choices, max_length=256,
                                    verbose_name=_('choose class'), null=True, blank=True)

    class Meta:
        verbose_name = _('main slide show')
        verbose_name_plural = _('main slide show')


class SlideShow(models.Model):
    title = models.CharField(default=None, max_length=32, verbose_name=_('title'))
    parent_category = models.ForeignKey(to=ParentCategory, verbose_name=_('parent category'), null=True, blank=True,
                                        on_delete=models.CASCADE, related_name="parent_category")
    category = models.ForeignKey(to=ProductCategory, verbose_name=_('category'), null=True, blank=True,
                                 on_delete=models.CASCADE, related_name='category')
    order_by = models.CharField(default='releaseDate', choices=orderByDict, max_length=256,
                                verbose_name=_('order by'))
    show_order = models.IntegerField(default=1, verbose_name=_('show order'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    is_delete = models.BooleanField(default=False, verbose_name='deleted')
    note = models.CharField(default=_('if you choose parent category, category not matter'),
                            max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('slide show')
        verbose_name_plural = _('slide shows')
