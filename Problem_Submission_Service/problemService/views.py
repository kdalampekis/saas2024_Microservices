from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import requests


import logging

logger = logging.getLogger(__name__)

class MetadataCreateView(APIView):
    def post(self, request, model_id):
        logger.debug(f'Received POST request for SolverModel model_id: {model_id}')
        try:
            solver_model = SolverModel.objects.get(model_id=model_id)
            logger.debug(f'SolverModel found: {solver_model}')
        except SolverModel.DoesNotExist:
            logger.error(f'SolverModel with model_id {model_id} not found')
            return Response({'error': 'SolverModel not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['problem_type'] = solver_model.model_id

        serializer = MetadataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, model_id):
        logger.debug(f'Received GET request for SolverModel model_id: {model_id}')
        try:
            solver_model = SolverModel.objects.get(model_id=model_id)
            logger.debug(f'SolverModel found: {solver_model}')
        except SolverModel.DoesNotExist:
            logger.error(f'SolverModel with model_id {model_id} not found')
            return Response({'error': 'SolverModel not found'}, status=status.HTTP_404_NOT_FOUND)

        metadata_entries = Metadata.objects.filter(problem_type=solver_model)
        serializer = MetadataSerializer(metadata_entries, many=True)
        return Response(serializer.data)



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

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def all_submissions(self, request):
        """
        This custom action returns all metadata entries.
        """
        metadata = Metadata.objects.all()
        serializer = self.get_serializer(metadata, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_submission(self, request, pk=None):
        """
        This custom action deletes a metadata entry based on its 'submission_id'.
        """
        try:
            metadata = Metadata.objects.get(submission_id=pk)
            metadata.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Metadata.DoesNotExist:
            return Response({'error': 'Metadata not found'}, status=status.HTTP_404_NOT_FOUND)
