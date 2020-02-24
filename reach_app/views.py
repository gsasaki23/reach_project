from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# GET for Index page
def index(request):
    return render(request, 'index.html')    

# GET for Dashboard page
def dashboard(request):
    try:
        context = {
            "current_user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'dashboard.html', context)
    except KeyError:
        return redirect('/')

# GET for New page
def new(request):
    try:
        context = {
            "current_user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'new.html', context)
    except KeyError:
        return redirect('/')

# GET for Stats page
def stats(request):
    try:
        context = {
            "current_user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'stats.html', context)
    except KeyError:
        return redirect('/')

# POST for register, route to dashboard if success
def attempt_reg(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')    
    
    else:
        # Hashing PW
        pw_hash= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        # Creates new User
        User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            password=pw_hash,
        )
        current_user = User.objects.last().id
        request.session['user_id'] = current_user.id
        return redirect('/dashboard')

# POST for login, route to dashboard if success
def attempt_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')    
    
    else:
        current_user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = current_user.id
        return redirect('/dashboard')


# POST for logging out, clearing session
def logout(request):
    del request.session['user_id']
    return redirect('/')