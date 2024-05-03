from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics

# from rest_framework.renderers import JSONRenderer

class LoginApiView(APIView):
#     renderer_classes = [JSONRenderer]

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
#             return redirect("main")
        else:
            return Response({"error": "Invalid credentials"}, status=400)

    def get(self, request, *args, **kwargs):
        print("get called")
        return render(request, "login.html")
    
    
    
class MainView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "main.html")