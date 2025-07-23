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

def add_course(request):
    if request.method == 'GET':
        # Retrieve 'title' and 'description' from GET parameters, default to empty string if not provided
        # Title = request.GET.get('title', '').strip()
        Title = request.GET.get('title')
        # Description = request.GET.get('description', '').strip()
        Description = request.GET.get('description')

        # Check if both fields have been filled
        if Title and Description:
            # Create and save new course if both fields are provided
            # new_course = Course(title=Title, description=Description)
            # new_course.save()
            Course.objects.create(title=Title, description=Description)
            

            # Optionally, add a success message or reset the form
            return render(request, 'courses_app/add_course.html', {
                'message': 'Course added successfully',
            })
        return render(request, 'courses_app/add_course.html')