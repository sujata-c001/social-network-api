from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate

from .models import LoginForm

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('posts')
        
        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'users/login.html',{'form': form})

def sign_up(request):
    pass

def profile(request):
    pass

def logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
