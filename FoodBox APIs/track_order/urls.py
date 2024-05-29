from django.urls import path
from .views import TrackOrderView, CreateTrackOrderView, UpdateTrackOrderStatusView

urlpatterns = [
    path('track_order/create/', CreateTrackOrderView.as_view(),
         name='create-TrackOrder'),
    path('track_order/<str:order_number>/',
         TrackOrderView.as_view(), name='track-order'),
    path('track_order/update/<str:order_number>/',
         UpdateTrackOrderStatusView.as_view(), name='update-order-status'),
]
