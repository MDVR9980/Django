from django.shortcuts import render
from courses_app.models import Course

def course_list(request):
    courses = Course.objects.all()

    return render(request, "courses_app/courses_list.html", context={"courses": courses})