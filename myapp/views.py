from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm

# Register View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    return render(request, 'login.html')



# Welcome View
def welcome_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'welcome.html')


# Logout View (Optional)
def logout_view(request):
    logout(request)
    return redirect('login')

def welcome_view(request):
    users = User.objects.exclude(last_login=None)  # Only users who have logged in
    return render(request, 'welcome.html', {'users': users})