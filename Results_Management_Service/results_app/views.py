from django.shortcuts import render
from django.http import JsonResponse
# from computation.models import Income
import requests
from .serializers import *
from rest_framework.response import Response

def fetch_income_data():
    try:
        response = requests.get('http://computation-service:8000/computation/api/problem/vehicle')
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()  # Parse JSON response
        # Deserialize the data
        deserializer = ProblemsDeserializer(data=data, many=True)
        deserializer.is_valid(raise_exception=True)
        return Response(deserializer.validated_data)
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e}")
        return []
    except ValueError as e:
        # Handle JSON decode error
        print(f"JSON decode error: {e}")
        return []

def income_data(request):
    income_data = fetch_income_data()
    return JsonResponse(income_data, safe=False)

# def income_data_2(request):
#     incomes = Income.objects.using('computationdb').all().values()
#     return JsonResponse(list(incomes), safe=False)
