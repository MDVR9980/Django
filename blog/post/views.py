from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from post.models import Article, Category, Comment, Message, User
from django.core.paginator import Paginator
from .forms import ContactUsForm, MessageForm
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.views.generic import ArchiveIndexView, YearArchiveView
from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CustomLoginrequiredMixins

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

def search(request):
    q = request.GET.get('q')
    articles = Article.objects.filter(title__icontains=q)

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

def contactus(request):
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            # title = form.cleaned_data['title']
            # text = form.cleaned_data['text']
            # email = form.cleaned_data['email']
            # Message.objects.create(title=title, text=text, email=email)
            # return redirect('home:main')
            form.save()
            return redirect('home:main')
    else:
        form = MessageForm()
    return render(request, "post/contact_us.html", {"form": form})

class TestBaseView(View):
    name = 'mdvr'
    def get(self, request):
        return HttpResponse(self.name)
    

# class ArticleList(ListView):
#     queryset = Article.objects.all()
#     template_name = "post/posts_list2.html"

class ArticleList(TemplateView):
    template_name = "post/posts_list2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Article.objects.all()
        return context


class UserList(ListView):
    queryset = User.objects.all()
    template_name = "post/user_list.html"


class HomePageRedirect(RedirectView):
    # url = '/articles/list'
    pattern_name = "post:posts_list"
    # permanent = False
    # query_string = False

    def get_redirect_url(self, *args, **kwargs):
        print(self.request.user.username)
        return super().get_redirect_url(*args, **kwargs)
    

class ArticleDetailView(DetailView):
    model = Article
    template_name = "post/post_detail.html"
    # context_object_name = "article" # by default : object or article
    # slug_field = "slug"
    # slug_url_kwarg = "slug"
    # pk_url_kwarg = "id"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['name'] = "mdvr"
    #     return context

    # queryset = Article.objects.filter(published=True)

# class ArticleListView(LoginRequiredMixin, ListView):
class ArticleListView(CustomLoginrequiredMixins, ListView):
    model = Article
    template_name = "post/posts_list.html"
    context_object_name = "articles"  # <- ensure this line exists
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # page_obj might be available via context['page_obj'] or context['articles']
        page_obj = context.get('page_obj') or context.get('articles')
        paginator = context.get('paginator')

        if page_obj and paginator:
            total_pages = paginator.num_pages
            current_page = getattr(page_obj, 'number', None)
            if current_page is not None:
                pages_to_show = 2
                start_page = max(current_page - pages_to_show, 1)
                end_page = min(current_page + pages_to_show, total_pages)

                context['page_range'] = range(start_page, end_page + 1)
                context['total_pages'] = total_pages
                context['current_page'] = current_page

        return context
    
    # queryset = Article.objects.filter(published=True)


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['name'] = "mdvr"
    #     return context


class ContactUsView(FormView):
    template_name = "post/contact_us.html"
    form_class = MessageForm
    # success_url = "/"
    success_url = reverse_lazy("home:main")

    def form_valid(self, form):
        form_data = form.cleaned_data
        # Message.objects.create(title=form_data['title'])
        Message.objects.create(**form_data)
        return super().form_valid(form)
    
class MessageView(CreateView):
    model = Message
    # fields = "__all__"
    fields = ('title', 'text', 'age')
    success_url = reverse_lazy("home:main") 
    # template_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.all()
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.email = self.request.user.email
        instance.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        print(self.object)
        return super(MessageView, self).get_success_url()
    

class MessageListView(ListView):
    model = Message

class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'text', 'age')
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("post:message_list")

class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("post:message_list")
    template_name_suffix = "_confirm_delete"


class ArchiveIndexArticleView(ArchiveIndexView):
    model = Article
    date_field = "updated"
    # template_name_suffix = 'article_archive' # by default : _archive
    # template_name = "article_archive"


class YearArchiveArticleView(YearArchiveView):
    model = Article
    date_field = "pub_date"
    make_object_list = True
    allow_future = True
    # template_name_suffix = '_archive_year' # by default : _archive_year
    # template_name = "article_archive_year"