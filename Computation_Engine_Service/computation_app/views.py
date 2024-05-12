from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .vrpSolver import main
import json
import subprocess
import os
import re
from .models import *



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
    # Assuming each list contains exactly one entry for simplicity, adjust as needed
    if objective:
        Objective.objects.create(value=int(objective[0]))

    if maximum:
        Maximum.objects.create(max_distance=int(maximum[0].replace('m', '')))

    # Assuming 'vehicles', 'routes', and 'distances' are lists with corresponding data
    for v_data, route, distance in zip(vehicles, routes, distances):
        # Extract vehicle ID; assuming it's the first element before the colon
        vehicle_id = int(v_data.split(':')[0].strip())
        distance = int(distance.replace('m', '').strip())

        # Check if Vehicle exists and update or create accordingly
        vehicle, created = Vehicle.objects.get_or_create(vehicle_id=vehicle_id)
        if created:
            vehicle.route = route
            vehicle.distance = distance
            vehicle.save()
        else:
            vehicle.add_route(route, distance)

def home(request):
    return HttpResponse("Welcome to My App!")

def index(request):
    return render(request, 'solver.html')

@csrf_exempt  # You can remove this if using CSRF tokens
@require_http_methods(["POST"])
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
            return JsonResponse({'error': 'No JSON file provided'}, status=400)

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

        print("Executing the VRP solver script...")

        print("Setting the script path")
        script_path = os.path.join(os.getcwd(), 'Scripts', 'vrpSolver.py')
        print(f"Script path: {script_path}")

    except Exception as e:
        print(f"First error: {str(e)}")




    try:
        result = subprocess.run(
            ['python', script_path, temp_file_path, number_of_locations, number_of_vehicles, vehicle_capacity],
            capture_output=True, text=True
        )


        if result.stderr:
            print(f"Script errors: {result.stderr}")
            return JsonResponse({'error': result.stderr}, status=400)

        print("Script execution completed.")
        if result.stdout:
            print(result)
            print(f"Script output: {result.stdout}")
            objective = []
            vehicles = []
            routes = []
            distances = []
            maximum = []
            objective, vehicles, routes, distances, maximum=parse_and_save_data(result.stdout)
            print("Now we see if the returned results are correct")
            print(objective, vehicles, routes, distances, maximum)
            save_route_data(objective, vehicles, routes, distances, maximum)

        return JsonResponse({'result':result.stdout}, status=200)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)