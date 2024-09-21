import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(['GET'])
def fetch_data(request, sub_id):  # Accept request and submission_id as arguments
    try:
        # URLs for the APIs, using Docker container names instead of localhost
        submission_url = f'http://problem-service:8000/problem/submission/{sub_id}/'
        result_url = f'http://computation-service:8000/computation/result/{sub_id}/'
        
        # Fetch data from submission API
        submission_response = requests.get(submission_url)
        submission_response.raise_for_status()  # Raise an error for bad status codes
        submission_data = submission_response.json()  # Parse JSON response

        # Fetch data from result API
        result_response = requests.get(result_url)
        result_response.raise_for_status()  # Raise an error for bad status codes
        result_data = result_response.json()  # Parse JSON response

        # Combine the data
        combined_data = {
            'submission_data': submission_data,
            'result_data': result_data,
        }

        return Response(combined_data)  # Directly return the combined JSON data

    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e}")
        return Response({"error": "Request error"}, status=500)
    except ValueError as e:
        # Handle JSON decode error
        print(f"JSON decode error: {e}")
        return Response({"error": "JSON decode error"}, status=500)
