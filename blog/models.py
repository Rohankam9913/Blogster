from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogModel(models.Model):
    TOPICS = [
        ("PR","Programming"),
        ("TC","Technology"),
        ("AT","Art"),
        ("DO","DevOps"),
        ("LT","Literature"),
        ("SC","Science")
    ]

    title = models.CharField(max_length=500)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add= True)
    topics = models.CharField(max_length=2,choices = TOPICS)
    claps = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class TopicModel(models.Model):
    TOPICS = [
        ("PR","Programming"),
        ("TC","Technology"),
        ("AT","Art"),
        ("DO","DevOps"),
        ("LT","Literature"),
        ("SC","Science")
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=2, choices=TOPICS)
    posts = models.IntegerField(default=0)

    def __str__(self):
        return self.name