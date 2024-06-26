from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views import CategoryViewSet, SubcategoryViewSet, ProductViewSet, ProductList

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('searchProduct/', ProductList.as_view(), name='product-searching'),
]
