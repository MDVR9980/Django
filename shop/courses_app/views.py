from django.shortcuts import render
from courses_app.models import Course

def course_list(request):
    courses = Course.objects.all()

    return render(request, "courses_app/courses_list.html", context={"courses": courses})

def course_detail(request, id):
    course = Course.objects.get(id=id)
    course.views += 1
    course.save()

    return render(request, "courses_app/course_detail.html", context={'course': course})
