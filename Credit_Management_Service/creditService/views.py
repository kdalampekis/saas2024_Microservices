from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import CreditTransaction, UserCreditBalance
from .serializers import UserCreditBalanceSerializer, CreditTransactionSerializer
import decimal
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model


class GetBalanceView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user_credit_balance = UserCreditBalance.objects.get(user_id=user_id)
        except UserCreditBalance.DoesNotExist:
            return Response({"detail": f"User {user_id} not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCreditBalanceSerializer(user_credit_balance)
        return Response(serializer.data)


User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class InitializeUserCreditBalanceView(APIView):

    def post(self, request):
        user_id = request.data.get('user_id')
        print(user_id)

        if not user_id:
            return Response({"detail": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user exists in the User table
        user, created = User.objects.get_or_create(username=user_id, defaults={'username': user_id})

        if created:
            # Optionally set other user fields if needed
            user.set_password(User.objects.make_random_password())
            user.save()

        # Create or get the UserCreditBalance
        user_credit_balance, created = UserCreditBalance.objects.get_or_create(
            user_id=user_id,  # Use the string user_id
            defaults={'balance': 0.00}
        )

        if not created:
            return Response({"detail": "User credit balance already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCreditBalanceSerializer(user_credit_balance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PurchaseCreditsView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreditTransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()

            # Update the user's credit balance
            user_credit_balance, created = UserCreditBalance.objects.get_or_create(user_id=transaction.user_id)
            user_credit_balance.balance += transaction.credits
            user_credit_balance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpendCreditsView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = get_object_or_404(User, username=user_id)
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