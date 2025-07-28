from django.shortcuts import render, get_object_or_404
from post.models import Article

def post_detail(request, slug):
    # article = Article.objects.get(id=pk)
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'post/post_detail.html', {'article': article})

def posts_list(request):
    articles = Article.objects.all()
    return render(request, "post/posts_list.html", {"articles": articles})
