from modeltranslation.translator import TranslationOptions, register
from .models import Product, ParentParentCategory, ParentCategory, ProductCategory


@register(Product)
class AccountTranslationOptions(TranslationOptions):
    fields = ['title', 'short_description', 'description']


@register(ParentParentCategory)
class AccountTranslationOptions(TranslationOptions):
    fields = ['title']


@register(ParentCategory)
class AccountTranslationOptions(TranslationOptions):
    fields = ['title']


@register(ProductCategory)
class AccountTranslationOptions(TranslationOptions):
    fields = ['title']
