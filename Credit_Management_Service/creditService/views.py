from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import CreditTransaction, UserCreditBalance
from .serializers import CreditTransactionSerializer, UserCreditBalanceSerializer
import decimal

class GetBalanceView(APIView):
#     permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User.objects.using('auth_db'), pk=user_id)
        user_credit_balance, created = UserCreditBalance.objects.get_or_create(user=user)
        serializer = UserCreditBalanceSerializer(user_credit_balance)
        return Response(serializer.data)

class PurchaseCreditsView(APIView):
#     permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreditTransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()

            # Update the user's credit balance
            user_credit_balance, created = UserCreditBalance.objects.get_or_create(user=transaction.user)
            user_credit_balance.balance += transaction.credits
            user_credit_balance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpendCreditsView(APIView):
#     permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        credits_to_spend = request.data.get('credits')

        if credits_to_spend is not None:
            credits_to_spend = decimal.Decimal(credits_to_spend)
            user_credit_balance, _ = UserCreditBalance.objects.get_or_create(user=user)

            if user_credit_balance.balance >= credits_to_spend:
                user_credit_balance.balance -= credits_to_spend
                user_credit_balance.save()

                # Log the transaction as a negative credit
                CreditTransaction.objects.create(user=user, credits=-credits_to_spend)

                serializer = UserCreditBalanceSerializer(user_credit_balance)
                return Response({
                    'status': 'Credits spent successfully',
                    'remaining_credits': serializer.data['balance']
                })
            else:
                return Response({'error': 'Insufficient credits'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid request, credits not provided'}, status=status.HTTP_400_BAD_REQUEST)
