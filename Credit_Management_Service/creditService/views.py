from rest_framework.views import APIView
from rest_framework.response import Response
from creditService.models import CreditTransaction
from django.db.models import Sum
from creditService.serializers import CreditTransactionSerializer
from rest_framework import status


class GetBalanceView(APIView):
    def get(self, request, user_id):
        total_credits = CreditTransaction.objects.filter(user_id=user_id).aggregate(Sum('credits'))['credits__sum'] or 0
        return Response({"user_id": user_id, "balance": total_credits})


class PurchaseCreditsView(APIView):
    def post(self, request):
        serializer = CreditTransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

