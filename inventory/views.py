from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from forms.forms import UserRegistrationForm, UserLoginForm


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({'message': 'User created successfully'}, status=201)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.session.get('next')
                if next_url:
                    del request.session['next']  # Remove 'next' from session to avoid redirection loops
                    return redirect(next_url)
                else:
                    return redirect('home')  # Redirect to home page if 'next' is not set
            else:
                form.add_error(None, 'Invalid credentials.')  # Add non-field error for invalid credentials
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'logout.html')


def api_authentication(request):
    api_key = request.headers.get('X-API-Key')
    if api_key == 'DoAndroidsDreamofElectricSheep':
        return JsonResponse({'message': 'Authentication successful'})
    else:
        return JsonResponse({'error': 'Invalid API key'}, status=401)


def home(request):
    return render(request, 'home.html')
