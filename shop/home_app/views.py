from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, "home_app/home.html")

def contactus(request):
    return HttpResponse("Contact us page")