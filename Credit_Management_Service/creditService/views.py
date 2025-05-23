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
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User

def get_user_id_by_username(request, username):
    user = get_object_or_404(User, username=username)
    return JsonResponse({'user_id': user.id})

class GetBalanceView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = get_object_or_404(User, username=user_id)
            user_credit_balance = UserCreditBalance.objects.get(user=user)
        except UserCreditBalance.DoesNotExist:
            return Response({"detail": f"User {user_id} not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCreditBalanceSerializer(user_credit_balance)
        return Response(serializer.data)


User = get_user_model()
'''
@method_decorator(csrf_exempt, name='dispatch')
class InitializeUserCreditBalanceView(APIView):

    def post(self, request):
        user_id = request.data.get('user_id')
        print(user_id)

        if not user_id:
            return Response({"detail": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user exists in the User table
        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            user = User(username=user_id)
            user.set_password(User.objects.make_random_password())
            user.save()

        # Create or get the UserCreditBalance
        user_credit_balance, created = UserCreditBalance.objects.get_or_create(
            user=user,
            defaults={'balance': 0.00}
        )

        if not created:
            print("User credit balance already exists")
            serializer = UserCreditBalanceSerializer(user_credit_balance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserCreditBalanceSerializer(user_credit_balance)
        return Response(serializer.data, status=status.HTTP_201_CREATED) '''

@method_decorator(csrf_exempt, name='dispatch')
class InitializeUserCreditBalanceView(APIView):

    def post(self, request):
        # Use 'username' for clarity instead of 'user_id'
        username = request.data.get('username')
        print(f"Username: {username}")

        # Validate if username is provided
        if not username:
            return Response({"detail": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists in the User table
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # If the user doesn't exist, create a new user
            user = User(username=username)
            user.set_password(User.objects.make_random_password())  # Set a random password for the new user
            user.save()

        # Create or get the UserCreditBalance entry for the user
        user_credit_balance, created = UserCreditBalance.objects.get_or_create(
            user=user,
            defaults={'balance': 0.00}  # Initialize credit balance to 0
        )

        if not created:
            print("User credit balance already exists")
            serializer = UserCreditBalanceSerializer(user_credit_balance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If the balance was newly created, return it with a status of 201 Created
        serializer = UserCreditBalanceSerializer(user_credit_balance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PurchaseCreditsView(APIView):
    # permission_classes = [IsAuthenticated]

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