from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .models import Metadata
from .serializers import MetadataSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets, status


# Create your views here.
def vehicle(request):
    return render(request, 'vehicle_solver.html')

def job_shop(request):
    return render(request, 'job_shop_solver.html')

def home(request):
    return HttpResponse("Welcome to My App!")


@api_view(['POST'])
def submit_problem(request, problem_name):
    try:
        # Collect all parameters from the request.POST dictionary
        parameters = request.POST.dict()
#         print(parameters)
        if not problem_name:
            return Response({"error": "problem_name is required"}, status=400)

        # Define the URL of the computation service
        url = f'http://computation-service:8000/computation/{problem_name}/'

        # Send a POST request with form data to the computation service
        response = requests.post(url, data=parameters)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the JSON response from the computation service
        data = response.json()
        return Response(data)  # Directly return the parsed JSON data

    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e}")
        return Response({"error": "Request error"}, status=500)

    except ValueError as e:
        # Handle JSON decode error
        print(f"JSON decode error: {e}")
        return Response({"error": "JSON decode error"}, status=500)



class MetadataViewSet(viewsets.ModelViewSet):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            # You can override this method to fetch the metadata using the submission_id
            metadata = Metadata.objects.get(submission_id=kwargs.get('pk'))
            metadata.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Metadata.DoesNotExist:
            return Response({'error': 'Metadata not found'}, status=status.HTTP_404_NOT_FOUND)