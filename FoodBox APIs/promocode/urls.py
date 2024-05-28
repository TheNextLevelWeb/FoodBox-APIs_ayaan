from django.urls import path
from .views import PromoCodeCreateView, PromoCodeDeleteView, PromoCodeCheckView

urlpatterns = [
    path('promocode/add/', PromoCodeCreateView.as_view(), name='addPromocode'),
    path('promocode/delete/<str:code>/',
         PromoCodeDeleteView.as_view(), name='deletePromocode'),
    path('promocode/check/', PromoCodeCheckView.as_view(), name='checkPromocode'),
    path('promocode/list/', PromoCodeCheckView.as_view(), name='checkPromocode'),
]
