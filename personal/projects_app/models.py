from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=35)
    address = models.CharField(max_length=150)
    image = models.ImageField(upload_to="project") 

    def __str__(self):
        return self.title