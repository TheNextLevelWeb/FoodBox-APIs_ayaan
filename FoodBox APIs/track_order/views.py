from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TrackOrder
from .serializers import TrackOrderSerializer, TrackOrderCreateSerializer, TrackOrderStatusUpdateSerializer


class TrackOrderView(generics.RetrieveAPIView):
    queryset = TrackOrder.objects.all()
    serializer_class = TrackOrderSerializer
    lookup_field = 'order_number'


class CreateTrackOrderView(APIView):

    def post(self, request):
        serializer = TrackOrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTrackOrderStatusView(APIView):
    def patch(self, request, order_number):
        try:
            order = TrackOrder.objects.get(order_number=order_number)
        except TrackOrder.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TrackOrderStatusUpdateSerializer(
            order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
