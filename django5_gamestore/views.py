from django.http import HttpResponseRedirect, JsonResponse
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
        "parentcategory_set", "parentcategory_set__productcategory_set")  # not sure but it may perform better :)

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


# not related to website
def nostr_view(request):
    name = request.GET.get('name', '')

    # response
    if name == "":
        response_data = {
            "error": "name parameter is missing"
        }
    elif name == "aghReza":
        response_data = {
            "names": {
                "aghReza": "b9c298ef367ab133e18b711e31ca3fde7bceed28e02aba00ca75269085e179b9"
            },
            # "relays": {
            #     "b9c298ef367ab133e18b711e31ca3fde7bceed28e02aba00ca75269085e179b9": ["wss://nos.lol/", "wss://relay.snort.social/"]
            # }
        }
    else:
        response_data = {
            "error": "name is not known"
        }

    return JsonResponse(response_data)
