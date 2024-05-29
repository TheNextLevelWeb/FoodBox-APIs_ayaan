from django.urls import path
from .views import CartListCreate, CartDetail

urlpatterns = [
    path('cart/', CartListCreate.as_view(), name='cart-list-create'),
    path('cart/<int:pk>/', CartDetail.as_view(), name='cart-detail'),
]
