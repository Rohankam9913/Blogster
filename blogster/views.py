from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'blogster/home.html')

def about(request):
    return render(request, 'blogster/about.html')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username = username)
        if not user.exists():
            messages.error(request, "User does not exists")
            return redirect("/login/")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Credentials")
            return redirect("/login/")
        
        login(request, user)
        if request.GET.get("next") is None:
            return redirect("/")

        return redirect(request.GET.get("next"))

    return render(request, 'blogster/login.html')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
    
        if user.exists():
            messages.error(request, "Account already exists")
            return redirect("/register")

        user = User.objects.create_user(
            username = username,
            password = password
        )

        user.save()
        return redirect("/")

    return render(request, 'blogster/register.html')

@login_required()
def logoutUser(request):
    logout(request)
    return redirect("/")

