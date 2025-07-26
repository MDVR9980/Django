from django.db import models
from django.contrib.auth.models import User

# Meny (article) To One (user):
# each acticle has only one author
# each user can has several article

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, )
    title = models.CharField(max_length=70)
    body = models.TextField()
    image = models.ImageField(upload_to="images/articles")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.body[:30]}"