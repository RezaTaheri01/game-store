from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-page'),
    # path('change-language/<str:lg>', views.change_language, name='change_language'),
    path('memory/', views.MemoryView.as_view(), name='memory_management'),
    path('first-follow/', views.FirstFollowView.as_view(), name='first_follow'),
    path('chain-rules/', views.ChainRulesView.as_view(), name='chain_rules'),
]
