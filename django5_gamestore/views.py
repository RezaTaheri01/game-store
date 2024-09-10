from django.http import HttpResponseRedirect
from django.shortcuts import reverse, render

from products.models import ParentParentCategory
from site_module.models import SiteSetting

# home page
def reDirect(request):
    reDirect_link = reverse('home-page')
    return HttpResponseRedirect(reDirect_link)


def header_partial(request):
    site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
    # category = ProductCategory.objects.filter(is_active=True, is_delete=False)
    parent_parent = ParentParentCategory.objects.filter(is_active=True, is_delete=False).prefetch_related(
        "parentcategory_set", "parentcategory_set__productcategory_set")  # not sure but it may perform fine :)
    return render(request, 'include/header_partial.html', context={
        # 'category': category,
        'main_category': parent_parent,
        'session': None,
        'site_setting': site_setting
    })


def footer_partial(request):
    site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
    return render(request, 'include/footer_partial.html', context={
        'site_setting': site_setting
    })


def logo_partial(request):
    site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
    return render(request, 'include/icon_partial.html', context={
        'site_setting': site_setting
    })


def preload_partial(request):
    site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
    return render(request, 'include/preload_partial.html', context={
        'site_setting': site_setting
    })
