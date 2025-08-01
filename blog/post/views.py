from django.shortcuts import render, get_object_or_404
from post.models import Article, Category, Comment
from django.core.paginator import Paginator

def post_detail(request, slug):
    # article = Article.objects.get(id=pk)
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)

    
    return render(request, 'post/post_detail.html', {'article': article})

def posts_list(request):
    articles = Article.objects.all()
    page_number = request.GET.get('page')  # Get current page number from URL
    paginator = Paginator(articles, 1)  # Number of articles per page
    objects_list = paginator.get_page(page_number)  # Get current page object

    total_pages = paginator.num_pages  # Total number of pages
    current_page = objects_list.number  # Current page number
    
    # Define how many pages to show before and after current page
    pages_to_show = 2

    # Calculate start and end of range using max and min to prevent out of bounds
    start_page = max(current_page - pages_to_show, 1)
    end_page = min(current_page + pages_to_show, total_pages)

    # Create the page range to be used in the template
    page_range = range(start_page, end_page + 1)

    # Pass all necessary data to template
    return render(request, "post/posts_list.html", {
        "articles": objects_list,
        "page_range": page_range,  # The range of pages to display
        "total_pages": total_pages,
        "current_page": current_page,
    })

def category_detail(request, pk=None):
    category = get_object_or_404(Category, id=pk)
    articles = category.articles.all()
    return render(request, "post/posts_list.html", {"articles": articles})