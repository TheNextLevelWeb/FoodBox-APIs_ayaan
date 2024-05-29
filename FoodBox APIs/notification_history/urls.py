from django.urls import path
from .views import NotiHistoryListCreate, NotiHistoryDelete

urlpatterns = [
    path('noti_history/', NotiHistoryListCreate.as_view(),
         name='notif_history-list-create'),
    path('noti_history/<int:pk>/', NotiHistoryDelete.as_view(),
         name='noti_history-delete'),
]
