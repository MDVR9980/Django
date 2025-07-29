from post.models import Article

def recent_articles(request):
    recent_articles = Article.objects.order_by('-created')

    return {"recent_articles": recent_articles}