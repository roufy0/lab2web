from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered! Please log in.')
            return redirect('users.login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'usermodule/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful. Welcome, {}!'.format(user.username))
            return redirect('books.index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'usermodule/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users.login')
