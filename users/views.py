from django.shortcuts import render

# Create your views here.
def register_login(request):
    return render(request, 'users/login_register.html')