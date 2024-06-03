from django.contrib import admin
from django.urls import path, include
admin.site.site_header = "FoodBox Admin"
admin.site.site_title = "FoodBox Admin Panel"
admin.site.index_title = "Welcome to FoodBox Admin Panel"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('shop.urls')),
    path('', include('promocode.urls')),
    path('', include('cart.urls')),
    path('', include('notification_history.urls')),
    path('', include('track_order.urls')),
]
