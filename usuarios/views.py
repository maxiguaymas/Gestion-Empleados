from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CaptchaAuthenticationForm
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'GET':
        # Limpiar variables de bloqueo al entrar a la página
        request.session['login_attempts'] = 0
        request.session['blocked_until'] = None
        request.session['block_count'] = 0
        return render(request, 'login.html', {'form': CaptchaAuthenticationForm()})

    if 'login_attempts' not in request.session:
        request.session['login_attempts'] = 0
    if 'blocked_until' not in request.session:
        request.session['blocked_until'] = None
    if 'block_count' not in request.session:
        request.session['block_count'] = 0

    blocked_until = request.session.get('blocked_until')
    bloqueado = False

    if blocked_until:
        blocked_until_time = timezone.datetime.fromisoformat(blocked_until)
        if timezone.now() < blocked_until_time:
            bloqueado = True
            delta = blocked_until_time - timezone.now()
            minutos, segundos = divmod(delta.seconds, 60)
            return render(request, 'login.html', {
                'form': CaptchaAuthenticationForm(),
                'error': f'Has superado el número máximo de intentos. Inténtalo de nuevo en <span id="tiempo-bloqueo">{minutos} m y {segundos} s</span>.',
                'bloqueado': True
            })
        else:
            request.session['login_attempts'] = 0
            request.session['blocked_until'] = None
            # No reinicies block_count aquí, así el tiempo sigue aumentando si vuelve a fallar
            return render(request, 'login.html', {
                'form': CaptchaAuthenticationForm()
            })

    form = CaptchaAuthenticationForm(request, data=request.POST)
    if not form.is_valid():
        request.session['login_attempts'] += 1
        if request.session['login_attempts'] >= 3:
            extra = 15 * request.session['block_count']
            bloqueo = 30 + extra
            blocked_until = timezone.now() + timedelta(seconds=bloqueo)
            request.session['blocked_until'] = blocked_until.isoformat()
            request.session['login_attempts'] = 0
            request.session['block_count'] += 1
            delta = blocked_until - timezone.now()
            minutos, segundos = divmod(delta.seconds, 60)
            return render(request, 'login.html', {
                'form': CaptchaAuthenticationForm(),
                'error': f'Has superado el número máximo de intentos. Inténtalo de nuevo en <span id="tiempo-bloqueo">{minutos} m y {segundos} s</span>.',
                'bloqueado': True
            })
        return render(request, 'login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos.'})

    # Si el login es exitoso, reinicia todo
    request.session['login_attempts'] = 0
    request.session['blocked_until'] = None
    request.session['block_count'] = 0
    auth_login(request, form.get_user())
    return redirect('index')
    
def logout(request):
    auth_logout(request)
    return redirect('index')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
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