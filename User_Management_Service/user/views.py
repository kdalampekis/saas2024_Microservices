from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

class UserDetailView(APIView):
    permission_classes = [IsAdminUser]  # Ensure only admins can access

    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, pk=user_id)
        return Response({
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active
        })

class UpdateUserCreditsView(APIView):
    permission_classes = [IsAdminUser]  # Ensure only admins can access

    def patch(self, request, user_id, format=None):
        user = get_object_or_404(User, pk=user_id)
        credits = request.data.get('credits')
        if credits is not None:
            user.credits = credits  # Assume 'credits' is a field on the User model
            user.save(update_fields=['credits'])
            return Response({'status': 'credits updated'})
        else:
            return Response({'error': 'Invalid request'}, status=400)
