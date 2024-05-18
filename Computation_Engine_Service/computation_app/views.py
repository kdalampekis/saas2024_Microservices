from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


import json
import subprocess
import os
import re
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status

from .Scripts.nQueens import solve_nqueens
from .Scripts.vrpSolver import main
################################################################
#API fetching problems
class IncomeData(APIView):
    def get(self, request):
        incomes = Problems.objects.all()
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data)


def parse_and_save_data(result):
    objective = []
    vehicles = []
    routes = []
    distances = []
    maximum = []
    print("In the parsing function")
    # Assuming output is a string that includes data in a predictable format
    lines = result.split('\n')

    # Iterate over each line and categorize it
    for line in lines:
        print(line)
        if line.startswith('Objective:'):
            objective.append(line.split(': ')[1])  # Assuming only one objective
        elif line.startswith('Route for vehicle'):
            vehicles.append(line)
        elif re.match(r'^\s*\d+ \s*->', line):  # Line starts with number followed by '->'
            routes.append(line)
        elif line.startswith('Distance of the route:'):
            distances.append(line.split(': ')[1])
        elif line.startswith('Maximum of the route distances:'):
            maximum.append(line.split(': ')[1])

    # Output each list to check
    print("Objective:", objective)
    print("Vehicles:", vehicles)
    print("Routes:", routes)
    print("Distances:", distances)
    print("Maximum:", maximum)

    return objective,vehicles,routes,distances,maximum

def save_route_data(objective, vehicles, routes, distances, maximum):
    if objective and vehicles and routes and distances and maximum:
        # Concatenate all route descriptions into one string
        route_descriptions = []
        for v_data, route, distance in zip(vehicles, routes, distances):
            try:
                vehicle_id = int(v_data.split()[3].strip(':'))  # Extract vehicle ID
                route_description = f"Route for vehicle {vehicle_id}: with route :{route} and distance of: {distance.strip()}m"
                route_descriptions.append(route_description)
            except ValueError as e:
                print(f"Error processing vehicle data: {e}")
                continue

        # Join all routes into a single text field
        routes_text = "\n\n".join(route_descriptions)
        # Create a new problem record
        Problems.objects.create(
            objective_id=int(objective[0]),
            number_of_vehicles=len(vehicles),
            routes=routes_text,
            maximum_distance=int(maximum[0].replace('m', ''))
        )

def home(request):
    return HttpResponse("Welcome to My App!")

def index(request):
    return render(request, 'solver.html')

@csrf_exempt  # You can remove this if using CSRF tokens
@api_view(["POST"])
def solve_vrp(request):
    try:
        print("Received a POST request.")

        # Handle file upload
        json_file = request.FILES.get('locations_file')
        if json_file:
            json_data = json.load(json_file)
            print("JSON file successfully loaded.")
        else:
            print("No JSON file provided.")
            return Response({'error': 'No JSON file provided'}, status=status.HTTP_400_BAD_REQUEST)

        number_of_locations = request.POST.get('number_of_locations')
        number_of_vehicles = request.POST.get('number_of_vehicles')
        vehicle_capacity = request.POST.get('vehicle_capacity')
        print(f"Received parameters - Number of Locations: {number_of_locations}, Number of Vehicles: {number_of_vehicles}, Vehicle Capacity: {vehicle_capacity}")

        # Store JSON data temporarily for script execution
        temp_file_path = 'temp_locations.json'
        with open(temp_file_path, 'w') as file:
            json.dump(json_data, file)
        print(f"Temporary JSON file created at {temp_file_path}")

        # Execute the Python script using subprocess
        script_path = os.path.join(os.getcwd(), 'Scripts', 'vrpSolver.py')
        print(f"Script path: {script_path}")

        result = subprocess.run(
            ['python', script_path, temp_file_path, number_of_locations, number_of_vehicles, vehicle_capacity],
            capture_output=True, text=True
        )

        if result.stderr:
            print(f"Script errors: {result.stderr}")
            return Response({'error': result.stderr}, status=status.HTTP_400_BAD_REQUEST)

        print("Script execution completed.")
        if result.stdout:
            print(f"Script output: {result.stdout}")
            # Assuming parse_and_save_data is a function that processes the script output
            objective, vehicles, routes, distances, maximum = parse_and_save_data(result.stdout)
            print(f"Parsed results: {objective}, {vehicles}, {routes}, {distances}, {maximum}")

        return Response({'result': result.stdout}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt  # You can remove this if using CSRF tokens
@api_view(['POST'])
def nqueens_api(request):
    try:
        # Extracting the board_size directly from request.POST
        board_size = request.POST.get('board_size')

        if board_size is None:
            return Response({'error': 'board_size is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert board_size to an integer
        try:
            board_size = int(board_size)
        except ValueError:
            return Response({'error': 'board_size must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate board_size
        if board_size < 1:
            return Response({'error': 'board_size must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming solve_nqueens is your function that solves the N-Queens problem
        solutions, stats = solve_nqueens(board_size)

        return Response({
            'board_size': board_size,
            'solutions': solutions,
            'stats': stats
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
