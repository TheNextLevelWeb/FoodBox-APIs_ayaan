from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PromoCode
from .serializers import PromoCodeSerializer
import logging

logger = logging.getLogger(__name__)


class PromoCodeCreateView(APIView):
    def post(self, request):
        logger.debug(f"Request data: {request.data}")
        serializer = PromoCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PromoCodeDeleteView(APIView):
    
    def delete(self, request, code):
        try:
            promo_code = PromoCode.objects.get(code=code)
            promo_code.delete()
            return Response("Deleted successfully",status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'detail': 'Promo code does not exist'}, status=status.HTTP_404_NOT_FOUND)


class PromoCodeCheckView(APIView):

    def get(self,request):
        promo_codes = PromoCode.objects.all()
        serializer = PromoCodeSerializer(promo_codes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'detail': 'Code not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            promo_code = PromoCode.objects.get(code=code)
            if promo_code.is_expired():
                return Response({'status': 'expired', 'discount': None}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'valid', 'discount': promo_code.discount}, status=status.HTTP_200_OK)
        except PromoCode.DoesNotExist:
            return Response({'status': 'invalid', 'discount': None}, status=status.HTTP_404_NOT_FOUND)
