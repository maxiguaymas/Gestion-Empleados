from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html',{'form': AuthenticationForm()})

    user = authenticate(
        request,
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is None:
        return render(request, 'login.html', {'form': AuthenticationForm(), 'error': 'Usuario o contraseña incorrectos.'})

    auth_login(request, user)
    return redirect('index')
    
def logout(request):
    auth_logout(request)
    return redirect('index')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': UserCreationForm()})
    
    if request.POST['password1'] != request.POST['password2']:
        return render(request, 'register.html', {'form': UserCreationForm(), 'error': 'Las contraseñas no coinciden.'})

    try:
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password1']
        )
        user.save()
        auth_login(request, user)
        return redirect('index')
    except:
        return render(request, 'register.html', {'form': UserCreationForm(), 'error': 'El Usuario ya existe.'})