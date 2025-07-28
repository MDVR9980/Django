from django.shortcuts import render
from post.models import Article

def post_detail(request, pk):
    article = Article.objects.get(id=pk)
    return render(request, 'post/post_detail', {'article': article})