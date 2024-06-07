import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
################################################################
import json
import subprocess
import os
import re
from .models import *
import numpy as np
import requests
################################################################
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import *
################################################################
from .Scripts.nQueens import solve_nqueens
from .Scripts.binPacking import bin_packing
from .Scripts.lpSolver import lp_solver
from .Scripts.jobShop import job_shop_solver
from .Scripts.mkp_solver import bin_packing_solver
from .Scripts.maxFlow import max_flow_solver
from .Scripts.sumAssignment import lin_sum_assignment
################################################################

def save_api_response(submission_id, api_name, response_data,time_taken):
    # Create and save the ApiResponse object
    Results.objects.create(
        submission_id=submission_id,
        problem_name=api_name,
        response_data=response_data,
        time_taken=time_taken
    )
    
    # Update the metadata status to 'executed'
    url = f"http://problem-service:8000/problem/change_status/{submission_id}/"
    requests.post(url)


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
        VRP.objects.create(
            objective_id=int(objective[0]),
            number_of_vehicles=len(vehicles),
            routes=routes_text,
            maximum_distance=int(maximum[0].replace('m', ''))
        )



@csrf_exempt
@api_view(["POST"])
def vrp_api(request):
    try:
        print("Received a POST request.")
        
        # Handle file upload
        if request.FILES:
            json_file = next(iter(request.FILES.values()))
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
        script_path = os.path.join(os.getcwd(), 'computationService', 'Scripts', 'vrpSolver.py')
        print(f"Script path: {script_path}")
        
        start_time = time.time()
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

            # save into seperate "vrp" model
            objective, vehicles, routes, distances, maximum = parse_and_save_data(result.stdout)
            print(f"Parsed results: {objective}, {vehicles}, {routes}, {distances}, {maximum}")
            save_route_data(objective, vehicles, routes, distances, maximum)    
            
            #save into general "problem" model
            result = {
                'result_id':objective,
                'vehicles':vehicles,
                'routes':routes,
                'distances':distances,
                'max_distance':maximum
            }
            # Measure end time and calculate duration
            submission_id = request.POST.get('submission_id')
            name = request.POST.get('name')
            end_time = time.time()
            duration = end_time - start_time
            save_api_response(submission_id, name, result, duration)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
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
        start_time = time.time()

        # Solve the N-Queens problem
        solutions, stats = solve_nqueens(board_size)

        # Measure end time and calculate duration
        end_time = time.time()
        duration = end_time - start_time
        result={
             'board_size': board_size,
             'solutions': solutions,
             'stats': stats
        }
        submission_id = request.POST.get('submission_id')
        name = request.POST.get('name')
        save_api_response(submission_id, name, result, duration)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def binpacking_api(request):
    weights_input = request.POST.get('weights')
    bin_capacity = request.POST.get('bin_capacity')

    if weights_input is None:
        return Response({"error": "weights is required"}, status=status.HTTP_400_BAD_REQUEST)

    if bin_capacity is None:
        return Response({"error": "bin_capacity is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Convert weights to a list of integers
    try:
        weights = [int(weight) for weight in weights_input.split(',')]
    except ValueError:
        return Response({"error": "Invalid weights provided. Ensure all weights are integers."}, status=status.HTTP_400_BAD_REQUEST)

    # Convert bin_capacity to an integer
    try:
        bin_capacity = int(bin_capacity)
    except ValueError:
        return Response({"error": "bin_capacity must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    start_time = time.time()
    result = bin_packing(weights, bin_capacity)
    end_time = time.time()
    duration = end_time - start_time
    submission_id = request.POST.get('submission_id')
    name = request.POST.get('name')
    save_api_response(submission_id, name, result, duration)
    
    return Response(result, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def linear_programming_api(request):
    try:
        # Get the JSON data from the request
        objective_coeffs_str = request.POST.get('objective_coeffs')
        constraints_coeffs_str = request.POST.get('constraints_coeffs')
        bounds_str = request.POST.get('bounds')

        # Convert JSON strings to Python lists
        objective_coeffs = json.loads(objective_coeffs_str)
        constraints_coeffs = json.loads(constraints_coeffs_str)
        bounds = json.loads(bounds_str)

        # Pair constraints coefficients with their bounds
        constraints = list(zip(constraints_coeffs, bounds))

        start_time = time.time()
        result = lp_solver(constraints, objective_coeffs)
        end_time = time.time()
        duration = end_time - start_time
        submission_id = request.POST.get('submission_id')
        name = request.POST.get('name')
        save_api_response(submission_id, name, result, duration)

        return Response(result, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format in request data"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def job_shop_api(request):
    try:
        # Get the jobs_data from the request
        jobs_data_str = request.POST.get('jobs_data')
        if not jobs_data_str:
            return Response({"error": "jobs_data is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert jobs_data from JSON string to Python list
        jobs_data = json.loads(jobs_data_str)

        start_time = time.time()
        result = job_shop_solver(jobs_data)
        end_time = time.time()
        duration = end_time - start_time
        submission_id = request.POST.get('submission_id')
        name = request.POST.get('name')
        save_api_response(submission_id, name, result, duration)

        return Response(result, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format in jobs_data"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def mkp_api(request):
    try:
        weights = json.loads(request.POST.get('weights'))
        values = json.loads(request.POST.get('values'))
        bin_capacity = int(request.POST.get('bin_capacity'))
        num_bins = int(request.POST.get('num_bins'))

        data = {
            "weights": weights,
            "values": values,
            "bin_capacity": bin_capacity,
            "num_bins": num_bins
        }


        start_time = time.time()
        result = bin_packing_solver(data)
        end_time = time.time()
        duration = end_time - start_time
        submission_id = request.POST.get('submission_id')
        name = request.POST.get('name')
        save_api_response(submission_id, name, result, duration)


        return Response(result, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format in request data"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def max_flow_api(request):
    try:


        start_nodes = json.loads(request.POST.get('start_nodes'))
        end_nodes = json.loads(request.POST.get('end_nodes'))
        capacities = json.loads(request.POST.get('capacities'))
        source = int(request.POST.get('source'))
        sink = int(request.POST.get('sink'))

        # Print the received data
        print("start_nodes:", start_nodes)
        print("end_nodes:", end_nodes)
        print("capacities:", capacities)
        print("source:", source)
        print("sink:", sink)

        start_time = time.time()
        result = max_flow_solver(start_nodes, end_nodes ,capacities, source, sink)
        end_time = time.time()
        duration = end_time - start_time
        submission_id = request.POST.get('submission_id')
        name = request.POST.get('name')
        save_api_response(submission_id, name, result, duration)
        
        return Response(result, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format in request data"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error H": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def lin_sum_assignment_api(request):
    try:

        costs_str = request.POST.get('costs')
        if not costs_str:
            return Response({"error": "costs is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert jobs_data from JSON string to Python list
        costs = np.array(json.loads(costs_str))

        print("costs:", costs)

        start_time = time.time()
        result = lin_sum_assignment(costs)
        end_time = time.time()
        duration = end_time - start_time
        submission_id = request.POST.get('submission_id')
        name = request.POST.get('name')
        save_api_response(submission_id, name, result, duration)
        return Response(result, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format in request data"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error H": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Sends all problem results from a specific category (or all of them, if no category is specified)
@api_view(['GET'])
def sent_data(request):
    # Get the 'name' parameter from the query parameters
    name = request.query_params.get('name', None)
    if name:
        print(name)
        incomes = Results.objects.filter(problem_name=name).values()
    else:
        incomes = Results.objects.all().values()
    return Response(incomes)


# Deletes the results of a problem (should not be called by itself, only through /metadata/delete)
@csrf_exempt
def delete_result_view(request, sub_id):
    if request.method == 'DELETE':
        try:
            result = get_object_or_404(Results, submission_id=sub_id)
            result.delete()
            return JsonResponse({'message': 'Result deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Results.DoesNotExist:
            return JsonResponse({'error': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Not useful, however it works
@csrf_exempt
def computation_view(request, problem_name):
    if request.method == 'POST':
        try:
            print("The problem name here is:",problem_name)
            problem_views = {
                'nqueens': nqueens_api,
                # Add other problem views here
            }

            if problem_name in problem_views:
                # Call the appropriate view function with the original request
                return problem_views[problem_name](request)
            else:
                return JsonResponse({"error": "Unknown problem_name"}, status=400)
        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({"error": "Processing error"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)