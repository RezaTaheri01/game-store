from modeltranslation.translator import TranslationOptions, register
from .models import SiteSetting, SlideShow, MainSlideShow


@register(SiteSetting)
class AccountTranslationOptions(TranslationOptions):
    fields = ['site_name', 'copy_right', 'services', 'about_us']


@register(SlideShow)
class AccountTranslationOptions(TranslationOptions):
    fields = ['title']
