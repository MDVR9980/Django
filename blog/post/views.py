from django.shortcuts import render, get_object_or_404
from post.models import Article

def post_detail(request, pk):
    # article = Article.objects.get(id=pk)
    article = get_object_or_404(Article, id=pk)
    return render(request, 'post/post_detail.html', {'article': article})