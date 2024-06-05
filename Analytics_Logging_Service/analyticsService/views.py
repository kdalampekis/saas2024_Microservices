from django.http import JsonResponse
import requests

def user_submissions(request, username):
    try:
        url = 'http://problem-service:8000/metadata/all_submissions/'
        response = requests.get(url)
        response.raise_for_status()
        submissions = response.json()
        
        # Filter submissions based on the username parameter
        user_submissions = [submission for submission in submissions if submission['username'] == username]
        
        return JsonResponse(user_submissions, safe=False)
    except requests.ConnectionError as e:
        print(f"Failed to connect to the submission service: {e}")
        return JsonResponse({"error": "Failed to connect to the submission service"}, status=500)
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return JsonResponse({"error": "HTTP error occurred"}, status=e.response.status_code)
    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)
