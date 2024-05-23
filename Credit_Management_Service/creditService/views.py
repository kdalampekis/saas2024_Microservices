from rest_framework.views import APIView
from rest_framework.response import Response
from creditService.models import CreditTransaction
from django.db.models import Sum
from creditService.serializers import CreditTransactionSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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

class UpdateUserCreditsView(APIView):
    permission_classes = [IsAuthenticated]  # Depending on your needs, this might be more restrictive

    def patch(self, request, user_id, format=None):
        user = get_object_or_404(User, pk=user_id)
        credits = request.data.get('credits')
        if credits:
            user.profile.credits = credits  # Assuming 'credits' is stored in a related Profile model
            user.profile.save()
            return Response({'status': 'User credits updated'})
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)