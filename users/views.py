from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import LoginForm, RegistrationForm, TestForm

def login_view(request):
    """
    Function based view for handling login
    """
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        form = LoginForm(request.POST or None)
        if request.POST and form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('/home')
        return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    Function based view for handling logout
    """
    logout(request)
    return redirect('/users/login?logout=1')

@login_required
def change_password(request):
    """
    Function based view for handling the changing of passwords
    """
    if request.method == 'POST':
        form = TestForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/home?success=1')
    else:
        form = TestForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

def register(request):
    """
    Function based view for handling registration
    """
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/home')
        else:
            form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

