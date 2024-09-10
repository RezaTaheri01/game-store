from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from account.models import User


# search Python Validator


class ParentParentCategory(models.Model):
    title = models.CharField(max_length=256, verbose_name=_('category title'), unique=True)
    slug = models.CharField(max_length=256, verbose_name=_('link'), unique=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_delete = models.BooleanField(verbose_name=_('deleted'))  # soft delete

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("grand parent category")
        verbose_name_plural = _("grand parents categories")


class ParentCategory(models.Model):
    parent_parent_category = models.ManyToManyField(ParentParentCategory, verbose_name=_('parent category'))
    title = models.CharField(max_length=256, verbose_name=_('category title'), unique=True)
    slug = models.CharField(max_length=256, verbose_name=_('link'), unique=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_delete = models.BooleanField(verbose_name=_('deleted'))  # soft delete

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('parent category')
        verbose_name_plural = _('parent categories')


class ProductCategory(models.Model):  # create new db to link to others
    parent_category = models.ManyToManyField(ParentCategory, verbose_name=_('parent category'))
    title = models.CharField(max_length=56, db_index=True, verbose_name=_('category title'), unique=True)
    url_title = models.CharField(max_length=280, db_index=True, verbose_name=_('link'), unique=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_delete = models.BooleanField(verbose_name=_('deleted'))  # soft delete

    def __str__(self):
        return self.title

    class Meta:  # config extra command for parent class
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')


class Product(models.Model):  # Auto Add Primary Key (DataBase)
    title = models.CharField(max_length=56, verbose_name=_('product title'), unique=True)
    image = models.ImageField(upload_to='images/products', null=True, verbose_name=_('product image'))
    image_bg = models.ImageField(upload_to='images/products', null=True, verbose_name=_('product bg image'))
    category = models.ManyToManyField(ProductCategory, verbose_name=_('category'))
    price = models.IntegerField(verbose_name=_('price'))
    inventory = models.IntegerField(validators=[MinValueValidator(0)], default=1, null=True,
                                    verbose_name=_('inventory'))
    short_description = models.CharField(max_length=224, db_index=True, verbose_name=_('short description'))
    description = models.TextField(db_index=True, verbose_name=_('description'))
    slug = models.SlugField(default="", max_length=224, unique=True,
                            verbose_name=_('link'))  # in slug field db_index's default is True
    addDate = models.DateField(verbose_name=_('add date'), editable=True, null=True, blank=True)
    releaseDate = models.DateField(verbose_name=_('release date'), blank=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_delete = models.BooleanField(verbose_name=_('deleted'))  # soft delete
    discount = models.IntegerField(default=0, choices=((i, i) for i in range(0, 96, 5)), verbose_name=_('discount'))
    author = models.ForeignKey(User, verbose_name=_('author'), on_delete=models.SET_NULL, editable=False,
                               null=True, blank=True)

    def __str__(self):
        return self.title

    def current_price(self):
        return int(self.price * (100 - self.discount) / 100)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title.lower())
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_page', args=[self.slug])

    def get_absolute_url_fa(self):  # need something like that for search list view
        Link = reverse('product_page', args=[self.slug])
        Link_List = Link.split('/')
        Link_List.insert(1, 'fa')
        Link = ''
        for L in Link_List:
            Link += L + '/'
        url = str(Link[0:len(Link) - 1])
        return url

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    parent = models.ForeignKey("ProductComment", null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name=_('parent comment'), related_name='sub_comment')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name=_('author'), null=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('add date'))
    comment = models.TextField(verbose_name=_('comment'))
    confirm_by_admin = models.BooleanField(default=True, verbose_name=_('confirm by admin'))  # default most be false!

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = _('product comment')
        verbose_name_plural = _('product comments')


class ProductVisit(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('product'))
    ip = models.CharField(max_length=25, verbose_name=_('user ip'))
    user = models.IntegerField(verbose_name=_('user id'), null=True, blank=True)

    class Meta:
        verbose_name = _('visits')
        verbose_name_plural = _('visits')


class ProductGallery(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('product'))
    image = models.ImageField(upload_to='images/gallery_product', verbose_name=_('gallery image'), null=True)

    class Meta:
        verbose_name = _('product gallery')
        verbose_name_plural = _('product gallery')

    def __str__(self):
        return self.product.title
# from product_module.models import Product
# add product :

# new_product = Product(title='The Last Of Us Part II', price=2500000)
# new_product.save
# Added
#
# Product.objects.all() : check added data
# result of above line is : <QuerySet [<Product: Product object (1)>, <Product: Product object (2)>]>
#
# Product.objects.all()[0].title
# result : 'The Last Of Us Part II'


# edit data:
# first_product=Product.objects.all()[0]
# first_product.rating=5
# first_product.save()

# remove product
# first_product=Product.objects.all()[0]
# Product.objects.all()[1].delete()

# create object
# Product.objects.create(title='horizon forbidden west', price=2000000, rating=5, short_description='')

# get
# in get command the value have to be unique!
# Product.objects.get(id=4) by id
# Product.objects.get(is_active=True)

# filter mostly like get, but it can return multi items
# Product.objects.filter(is_active=False)
# Product.objects.filter(is_active=False,rating=5)
# rating__lt :lower than
# rating__lte :lower than or equal:
# Product.objects.filter(is_active=False, rating__lt=5)
# rating__gt :greater than
# rating__gte :greater than or equal:
# Product.objects.filter(is_active=False, rating__gt=4)

# search django filter
# Product.objects.filter(title__contains='last') and many more

# or
# from django.db.models import Q
# Product.objects.filter(Q(title__contains='last') | Q(short_description__contains='lies'))
# Product.objects.filter(Q(title__contains='last') | Q(short_description__contains='lies'),rating__gte=4) use or + and
# first Q section !

# extract data from linked db
# Product.objects.filter(category__url_title='open-world-games')
# same result
# Product.objects.filter(category__url_title__contains='open-')
# <link_db_name>__<section_name>

# extract data by linked db
# open_world=ProductCategory.objects.get(url_title='open-world-games')
# open_world.product_set.all()
# product_set is a related name and can be change in category field !


# add tag to product
# TLOU2 = Product.objects.all()[0]
# create a tag (Survival)
# save tag
# TLOU2.tags.add(Survival)

# get product related to tag
# game=ProductTags.objects.all()[0]
# game.product_set.all()

# class ProductTags(models.Model):
#     title = models.CharField(max_length=224, db_index=True, verbose_name='عنوان تگ')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')
#
#     class Meta:
#         verbose_name = 'تگ محصولات'
#         verbose_name_plural = 'تگ های محصولات'
#
#     def __str__(self):
#         return self.title
