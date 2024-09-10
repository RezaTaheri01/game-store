from rest_framework import serializers
from .models import SiteSetting, SlideShow
from products.models import Product


class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = "__all__"


class SlideShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideShow
        fields = "__all__"


class MainSlideShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'image_bg', 'price', 'inventory', 'releaseDate', 'discount']
