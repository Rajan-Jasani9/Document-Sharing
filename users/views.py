from django.shortcuts import render, redirect

from .models import User
from django.contrib.auth import authenticate, login

from django.contrib import messages

# Create your views here.
def register_login(request):
    return render(request, 'users/login_register.html')

    
def login_user(request):
    '''
    '''
    username = request.POST.get('email')
    password = request.POST.get('password')
    
    user = authenticate(request, email=username, password=password)
    if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page.
    else:
        messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login_register.html')

def register(request):
    '''
    '''
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    date_of_birth = request.POST.get('date_of_birth')
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    if User.objects.filter(username=email).exists():
            messages.error(request, 'User with this email already exists.')
    else:
        # Create the user
        user = User.objects.create(username=email, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        
        messages.success(request, 'User created successfully!')

        # Optionally, you can log the user in after registration
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page.
    return render(request, 'users/login_register.html')