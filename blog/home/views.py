from django.shortcuts import render
from post.models import Article

def home(request):
    articles = Article.objects.all()
    return render(request, "home/index.html", {'articles': articles})