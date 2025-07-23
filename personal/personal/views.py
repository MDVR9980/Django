from django.shortcuts import render
from projects_app.models import Project

def home(request):

    projects = Project.objects.all()

    return render(request, 'index.html', context={'projects':projects})