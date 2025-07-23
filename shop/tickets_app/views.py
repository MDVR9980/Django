from django.shortcuts import render
from tickets_app.models import Ticket

def add_ticket(request):
    if request.method == 'GET':
        # Retrieve 'title' and 'description' from GET parameters, default to empty string if not provided
        # Title = request.GET.get('title', '').strip()
        Title = request.GET.get('title')
        # Body = request.GET.get('body', '').strip()
        Body = request.GET.get('body')

        # Check if both fields have been filled
        if Title and Body:
            # Create and save new ticket if both fields are provided
            # new_ticket = Ticket(title=Title, body=Body)
            # new_ticket.save()
            Ticket.objects.create(title=Title, body=Body)

            # Optionally, add a success message or reset the form
            # return render(request, 'tickets_app/add_ticket.html', {
            #     'message': 'Ticket added successfully',
            # })
        return render(request, 'tickets_app/add_ticket.html')    