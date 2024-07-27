from django.urls import path
from . import views

urlpatterns = [
    path('write/', views.writeBlog, name="write"),
    path('read/', views.readBlog, name="read"),
    path('topics/', views.topics, name="topics"),
    path('read/<str:title>/<int:id>', views.singleBlog, name="singleBlog"),
    path('tag/<str:topicName>', views.singleTopic, name="postTag"),
    path('your_blogs/<str:authorId>', views.UserBlogs, name="yourBlogs"),
    path('delete_blog/<str:blogId>/<str:blogTopic>',views.deleteBlog, name="delete"),
    path('edit_blog/<str:blogId>', views.editBlog, name="edit"),
    
    path('searchBlogs/', views.searchBlogs, name="search")
]