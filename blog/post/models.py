from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Meny (article) To One (user):
# each acticle has only one author
# each user can has several article
# USER -> DELETE
# cascade
# set null
# set default
# protect
# do nothing

# class ArticleManager(models.Manager):

#     def get_queryset(self):
#         return super(ArticleManager, self).get_queryset().filter(status=True)

#     def counter(self):
#         return len(self.all()) 
    
#     def published(self):
#         return self.filter(published=True)

class Article(models.Model):
    # author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='1')
    # author = models.ForeignKey(User, on_delete=models.PROTECT)
    # author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='articles')
    title = models.CharField(max_length=70, unique_for_date='pub_date')
    body = models.TextField()
    image = models.ImageField(upload_to="images/articles")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pub_date = models.DateField(default=timezone.now)
    is_published = models.DurationField(default=timezone.timedelta(days=30, hours=0, minutes=0, seconds=0))
    myfile = models.FileField(upload_to='test', null=True)
    status = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, unique=True)
    pub_date = models.DateTimeField(default=timezone.now())
    floatfield = models.FloatField(default=1)
    myfile = models.FileField(upload_to='test', null=True)

    class Meta:
        ordering = ('-created',)

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        self.slug = slugify(self.title)
        super(Article, self).save()

    def get_absolute_url(self):
        return reverse("post:post_detail", kwargs={"slug": self.slug})
    

    # objects = ArticleManager()
    # objects = models.Manager()
    # custom_manager = ArticleManager()
    
    def __str__(self):
        return f"{self.title} - {self.body[:30]}" 
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', null=True, blank=True , on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
    
class Message(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    email = models.EmailField()
    age = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title