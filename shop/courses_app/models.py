from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=50)
    discription = models.TextField()
    situation = models.BooleanField(default=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title