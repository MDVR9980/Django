from post.models import Article, Category

def recent_articles(request):
    recent_articles = Article.objects.order_by('-created')

    return {"recent_articles": recent_articles}

def categories_list(request):
    categories =  Category.objects.all()
    
    return {"categories": categories}