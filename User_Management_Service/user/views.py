import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def fetch_submissions():
    try:
        url = f'http://problem-service:8000/metadata/all_submissions/'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError as e:
        print(f"Failed to connect to the submission service: {e}")
        return None
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None

def submissions_view(request):
    submissions = fetch_submissions()
    if submissions is None:
        return JsonResponse({'error': 'Failed to fetch data from submission service'}, status=500)
    return JsonResponse(submissions, safe=False)


@csrf_exempt
def delete_metadata_view(request, submission_id):
    if request.method == 'DELETE':
        url = f"http://problem-service:8000/metadata/{submission_id}/delete_submission/"
        response = requests.delete(url)
        if response.status_code == 204:
            return JsonResponse({'message': 'Metadata successfully deleted.'}, status=204)
        else:
            return JsonResponse({'error': response.text}, status=response.status_code)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)