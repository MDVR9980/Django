from django.shortcuts import render
from django.http import Http404

users = [
    {
        "name": "Davood",
        "username": "mdvr9980",
        "city": "Mashhhad",
    },
    {
        "name": "Rahmat",
        "username": "wolf2022",
        "city": "mashhad",
    },
    {
        "name": "Danial",
        "username": "dani9985",
        "city": "mashhad",
    }
]

def userslist(request):
    # users_list = users
    return render(request, 'accounts_app/user_list.html', context={'users_list': users})

def profile(request, username):
    for user in users:
        if user["username"] == username:
            return render(request, "accounts_app/profile.html", context={"user": user}) 
    raise Http404("This user is not exist")

def info(request):
    return render(request, "accounts_app/info.html")