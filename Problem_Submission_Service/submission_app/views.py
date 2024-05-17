from django.shortcuts import render

# Create your views here.
def vehicle(request):
    return render(request, 'vehicle_solver.html')

def job_shop(request):
    return render(request, 'job_shop_solver.html')

def home(request):
    return HttpResponse("Welcome to My App!")