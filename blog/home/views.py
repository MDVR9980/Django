from django.shortcuts import render
from post.models import Article

def home(request):
    articles = Article.objects.all()
    # recent_articles = Article.objects.all().order_by('-created')

    # articles = Article.objects.published() 
    # print(Article.objects.counter())
    
    return render(request, "home/index.html", {'articles': articles})