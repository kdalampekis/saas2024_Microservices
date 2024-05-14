from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User



class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        print("post called")
#         print("Request data:", request.data)
        username = request.data.get('username')
        password = request.data.get('password')
#         print(request.data)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                'token': token.key,
                'is_superuser': user.is_superuser
            }
            return Response(response_data)
#             return redirect("/logout")
        else:
            return Response({"error": "Invalid credentials"}, status=400)

    def get(self, request, *args, **kwargs):
        print("get called")
        return render(request, "login.html")




class SignUpApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("signup post called")
        username = request.data.get('username')
        password = request.data.get('password')
        # Create a new user with the provided information
        user = User.objects.create_user(username=username, password=password, is_active=False, is_superuser = False)

        token = Token.objects.create(user=user)

        return Response({"detail": "User created successfully. Activation required."}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        return render(request, "signup.html")




class LogoutApiView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the token from the request header
        token_header = self.request.META.get('HTTP_AUTHORIZATION')
        if token_header:
            # Find the user associated with the token
            try:
                user = Token.objects.get(key=token_header).user
            except Token.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Delete the token
            Token.objects.filter(user=user).delete()

            return Response({"detail": "Successfully logged out and deleted auth token."},status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token format."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return render(request, "logout.html")



# Html template to test google functionality
class GoogleApiView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "google.html")




# Custom logout function to test the google functionality
# Replace with the LogoutApiView when testing with tokens
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/login')  # Redirects the user to the login page after logout

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, pk=user_id)
        return Response({
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active
        })





# from django.contrib.auth import logout
# from django.shortcuts import redirect
#
# def social_login(request, backend):
#     # Log out any currently logged-in user
#     logout(request)
#     # Redirect to the social auth's begin process for the specified backend
#     return redirect('social:begin', backend=backend)

