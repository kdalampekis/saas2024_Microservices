import requests
from django.http import JsonResponse

def fetch_submissions():
    try:
        url = f'http://problem-service:8000/submissions/metadata/'
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


def delete_metadata(submission_id):
    url = f"http://problem-service:8003/metadata/delete/{submission_id}/"
    response = requests.delete(url)
    if response.status_code == 204:
        return "Metadata successfully deleted."
    else:
        return f"Error: {response.status_code}, {response.text}"
