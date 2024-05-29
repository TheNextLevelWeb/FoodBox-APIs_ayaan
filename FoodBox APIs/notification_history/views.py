from rest_framework import generics
from .models import NotiHistory
from .serializers import NotiHistorySerializer


class NotiHistoryListCreate(generics.ListCreateAPIView):
    queryset = NotiHistory.objects.all()
    serializer_class = NotiHistorySerializer


class NotiHistoryDelete(generics.DestroyAPIView):
    queryset = NotiHistory.objects.all()
    serializer_class = NotiHistorySerializer
