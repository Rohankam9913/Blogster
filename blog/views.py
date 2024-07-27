from django.shortcuts import render, redirect
from .forms import CreateForm
from django.http import HttpResponse
from .models import BlogModel, TopicModel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def writeBlog(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user

            # Updating the post count for a specific topic
            topic = request.POST["topics"]
            get_topic_info = TopicModel.objects.get(category=topic)
            get_topic_info.posts = get_topic_info.posts+1
            get_topic_info.save()
            
            form.save()
            return redirect("/blog/read")
    else:
        form = CreateForm()

    return render(request, 'blog/createBlog.html', { "form": form })

@login_required
def readBlog(request):
    blogs = BlogModel.objects.all()

    if len(blogs) == 0:
        return render(request, 'fallback.html', {"message": "No Blogs to show"})

    return render(request, 'blog/readBlog.html', {"blogs": blogs})

@login_required
def singleBlog(request, title, id):
    try:
        blogContent = BlogModel.objects.get(id=id)
        return render(request, 'blog/singleBlog.html', {'blogContent': blogContent})
    except:
        return render(request, 'fallback.html', {"message": "Blog does not exist"})

@login_required
def singleTopic(request, topicName):
    blogs = BlogModel.objects.filter(topics=topicName)

    if len(blogs) == 0:
        return render(request, 'fallback.html', {"message": "Nothing to show"})

    return render(request, 'blog/readBlog.html', {'blogs': blogs})

@login_required
def UserBlogs(request, authorId):
    try:
        yourBlogs = BlogModel.objects.filter(author=authorId)
        author = User.objects.get(id=authorId)
        
        if len(yourBlogs) == 0:
            return render(request, 'fallback.html', {"message": "Nothing to show"})

        return render(request, 'blog/readBlog.html', {'blogs': yourBlogs, 'author': author})
    except:
        return render(request, 'fallback.html', {"message": "Blog does not exist"})

@login_required
def topics(request):
    get_topics = TopicModel.objects.all()
    return render(request, 'blog/topics.html', {'topics': get_topics})

@login_required
def deleteBlog(request, blogId, blogTopic):
    blog = BlogModel.objects.filter(id=blogId)

    if len(blog) == 0:
        return render(request, 'fallback.html', {"message": "Blog your are trying to delete does not exist"})

    # Updating the post count for a specific topic
    if request.user == blog[0].author:
        blog.delete()
        get_topic_info = TopicModel.objects.get(category=blogTopic)
        get_topic_info.posts = get_topic_info.posts-1
        get_topic_info.save()
    else:
        return render(request, 'fallback.html', {"message": "Blog you are trying to delete is not posted by you!!!"})
    
    return redirect('read')

@login_required
def editBlog(request, blogId):
    try:
        blog = BlogModel.objects.get(id=blogId)
       
        if blog.author == request.user: 
            if request.method == "POST":
                form = CreateForm(request.POST, instance = blog)
                if form.is_valid():
                    blog = form.save(commit=False)
                    blog.author = request.user
                    blog.save()
                    return redirect("/blog/read")
            else:
                form = CreateForm(instance = blog)

            return render(request, "blog/editBlog.html", {"form": form})

        else:
            return render(request, "fallback.html", {"message": "Blog you are trying to edit is not posted by you !!!"})

    except:
        return render(request, "fallback.html",{"message": "Blog your trying to edit does not exists !!!"})

@login_required
def searchBlogs(request):
    search_query = request.GET.get("search_query")
    blogs = BlogModel.objects.filter(title__contains=search_query)
    if not blogs:
        return render(request, 'fallback.html', {"message": f"No search results found for '{search_query}' "})

    return render(request, "blog/readBlog.html" ,{'blogs': blogs})
