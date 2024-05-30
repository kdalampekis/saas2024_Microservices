from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from .serializers import *
import requests
import logging

logger = logging.getLogger(__name__)



class MetadataCreateView(APIView):
    def post(self, request, solver_name):
        logger.debug(f'Received POST request for SolverModel solver_name: {solver_name}')
        try:
            solver_model = SolverModel.objects.get(name=solver_name)
            logger.debug(f'SolverModel found: {solver_model}')
        except SolverModel.DoesNotExist:
            logger.error(f'SolverModel with name {solver_name} not found')
            return Response({'error': 'SolverModel not found'}, status=status.HTTP_404_NOT_FOUND)

        metadata_data = {
            'username': request.data.get('username'),
            'credit_cost': request.data.get('credit_cost'),
            'model_id': solver_model.model_id
        }

        metadata_serializer = MetadataSerializer(data=metadata_data)
        if metadata_serializer.is_valid():
            metadata = metadata_serializer.save()

            # Exclude 'username', 'credit_cost', and files from input_data
            input_data = {key: value for key, value in request.data.items() if key not in ['username', 'credit_cost'] and key not in request.FILES}

            # Extract the file, if there is any
            input_file = None
            for file in request.FILES:
                input_file = request.FILES[file]
                print("file:", input_file)
                break
                
            # If there is additional input data or a file, save it
            if input_data or input_file:
                input_serializer = InputSerializer(data={
                    'metadata': metadata.submission_id,
                    'input_data': input_data,
                    'input_file': input_file
                })
                if input_serializer.is_valid():
                    input_serializer.save()

            return Response(metadata_serializer.data, status=status.HTTP_201_CREATED)
        return Response(metadata_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, solver_name):
        logger.debug(f'Received GET request for SolverModel solver_name: {solver_name}')
        try:
            solver_model = SolverModel.objects.get(name=solver_name)
            logger.debug(f'SolverModel found: {solver_model}')
        except SolverModel.DoesNotExist:
            logger.error(f'SolverModel with name {solver_name} not found')
            return Response({'error': 'SolverModel not found'}, status=status.HTTP_404_NOT_FOUND)

        metadata_entries = Metadata.objects.filter(model_id=solver_model.model_id)
        serializer = MetadataSerializer(metadata_entries, many=True)
        return Response(serializer.data)



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
        return JsonResponse(serializer.data, safe=False)

    @action(detail=True, methods=['delete'], permission_classes=[AllowAny])
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



@api_view(['POST'])
def submit_problem(request, sub_id):
    try:
        metadata = get_object_or_404(Metadata, submission_id=sub_id)
        # Change the status to 'not ready
        metadata.is_ready = False
        metadata.save()
        
        # Get the problem name, as written in the URL
        problem_name = metadata.model_id.name
        
        # Get the inputs associated with the metadata
        inputs = Input.objects.filter(metadata=metadata)
        
        if not inputs.exists():
            return Response({"error": "No inputs found for this submission"}, status=400)
        
        # Define the URL of the computation service
        url = f'http://computation-service:8000/computation/{problem_name}/'

        # Prepare data and files for the request
        data = {}
        files = {}

        for input in inputs:
            if input.input_data:
                data.update(input.input_data)
            if input.input_file:
                files[input.input_file.name] = input.input_file

        data['submission_id'] = sub_id
        data['name'] = metadata.model_id.title
        
        # Send a POST request with form data and files to the computation service
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the JSON response from the computation service
        response_data = response.json()
        return Response(response_data)  # Directly return the parsed JSON data

    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        logger.error(f"Request error: {e}")
        return Response({"error": "Request error"}, status=500)

    except ValueError as e:
        # Handle JSON decode error
        logger.error(f"JSON decode error: {e}")
        return Response({"error": "JSON decode error"}, status=500)
    except Metadata.DoesNotExist:
        return Response({"error": "Metadata not found"}, status=404)
    except Input.DoesNotExist:
        return Response({"error": "Input not found"}, status=404)



def initialize_solver_models(request):
    if request.method == 'GET':
        solver_models = [
            {"title": "Vehicle Routing Problem (VRP)", "name": "vrp", "notes": "Solves the problem of routing vehicles to service a set of locations in an optimal manner."},
            {"title": "N-Queens Problem", "name": "queens", "notes": "Solves the classic N-Queens puzzle, where N queens must be placed on an NxN chessboard such that no two queens attack each other."},
            {"title": "Bin Packing", "name": "bin_packing", "notes": "Solves the problem of packing objects of different volumes into a finite number of bins in a way that minimizes the number of bins used."},
            {"title": "Job Shop Scheduling", "name": "job_shop", "notes": "Solves the scheduling problem where a set of jobs are processed on a set of machines with the goal of optimizing production."},
            {"title": "Linear Programming Solver", "name": "linear_programming", "notes": "Solves optimization problems where some or all of the variables are required to be integers."},
            {"title": "Maximum Flow", "name": "max_flow", "notes": "Solves the problem of finding the maximum feasible flow in a flow network."},
            {"title": "Multiple Knapsack Problem (MKP)", "name": "multiple_knapsack", "notes": "Solves the problem of assigning items with given weights and values to multiple knapsacks to maximize the total value."},
            {"title": "Assignment Problem", "name": "lin_sum_assignment", "notes": "Solves the problem of assigning resources to tasks in a way that minimizes the total cost or maximizes the total profit."}
        ]
        
        for model in solver_models:
            title = model['title']
            if not SolverModel.objects.filter(name=model['name']).exists():
                SolverModel.objects.create(title=model['title'], name=model['name'], notes=model['notes'])
                print(f'Model {title} added.')
            else:
                print(f'Model {title} already exists, skipping.')
        
        return JsonResponse({"success": 200}, status=200)



@csrf_exempt
def change_metadata_status(request, sub_id):
    if request.method == 'POST':
        # Retrieve the Metadata object with the given submission_id
        meta = get_object_or_404(Metadata, submission_id=sub_id)
        
        # Update the metadata attributes
        meta.is_executed = True
        meta.save()
        
        # Return a JSON response indicating success
        return JsonResponse({'message': 'Computation completed successfully'}, status=200)
    else:
        # Return a method not allowed response for non-POST requests
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)



def vehicle(request):
    return render(request, 'vehicle_solver.html')


def job_shop(request):
    return render(request, 'job_shop_solver.html')