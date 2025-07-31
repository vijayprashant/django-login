from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.utils.timezone import localtime
from django.utils.timezone import now

# Register View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Optional: strong password check (basic)
        import re
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!#%*?&])[A-Za-z\d@$!#%*?&]{8,}$', password1):
            messages.error(request, "Password must be at least 8 characters, include 1 uppercase, 1 number, and 1 special character.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password1)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')

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
    users = User.objects.all().order_by('-date_joined')  # Recent first
    total_users = users.count()
    login_time = localtime(request.session.get('login_time'))

    return render(request, 'welcome.html', {
        'user': request.user,
        'login_time': login_time,
        'total_users': total_users,
        'users': users,
    })

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')
