from django.contrib import admin
from .models import BlogModel, TopicModel

# Register your models here.
admin.site.register(BlogModel)
admin.site.register(TopicModel)