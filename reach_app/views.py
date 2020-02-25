from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime


# GET for Index page
def index(request):
    return render(request, 'index.html')

# GET for Dashboard page
def dashboard(request):
    try:
        refresh_followups()
        
        code_21 = Position.objects.filter(status_code = 21)
        code_22 = Position.objects.filter(status_code = 22)
        code_23 = Position.objects.filter(status_code = 23)
        reached_positions = code_21 | code_22 | code_23
        reached_positions.order_by("status_code")
        
        code_2 = Position.objects.filter(status_code = 2)
        code_3 = Position.objects.filter(status_code = 3)
        code_4 = Position.objects.filter(status_code = 4)
        code_12 = Position.objects.filter(status_code = 12)
        code_13 = Position.objects.filter(status_code = 13)
        code_14 = Position.objects.filter(status_code = 14)
        todo_positions = code_2 | code_3 | code_4 | code_12 | code_13 | code_14
        todo_positions.order_by("updated_at")
        
        code_1 = Position.objects.filter(status_code = 1)
        code_11 = Position.objects.filter(status_code = 11)
        waiting_positions = code_1 | code_11
        waiting_positions.order_by("updated_at")
        
        code_31 = Position.objects.filter(status_code = 31)
        code_32 = Position.objects.filter(status_code = 32)
        code_33 = Position.objects.filter(status_code = 33)
        code_34 = Position.objects.filter(status_code = 34)
        obsolete_positions = code_31 | code_32 | code_33 | code_34
        obsolete_positions.order_by("updated_at")
        
                
        context = {
            "current_user": User.objects.get(id=request.session['user_id']),
            "today_date": datetime.now().date(),
            # Area 1
            "reached_positions": reached_positions,
            # Area 2
            "todo_positions": todo_positions,
            # Area 3
            "waiting_positions": waiting_positions,
            # Area 4
            "obsolete_positions": obsolete_positions,
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

# GET for Edit page
def edit(request, position_id):
    try:
        context = {
            "current_user": User.objects.get(id=request.session['user_id']),
            "position": Position.objects.get(id=position_id)
        }
        return render(request, 'edit.html', context)
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
        pw_hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()

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

# POST for new position, route to dashboard if success
def attempt_position(request):
    # TODO add to existing company
    # Creates new company
    Company.objects.create(
        name=request.POST["company_name"],
        info=request.POST["company_info"],
    )
    
    # Creates new position
    Position.objects.create(
        user=User.objects.get(id=request.session['user_id']),
        title=request.POST["title"],
        location=request.POST["location"],
        salary=request.POST["salary"],
        posting=request.POST["posting"],
        company=Company.objects.last(),
    )
    return redirect('/dashboard')

# POST for updating status code, refresh dashboard
def update_status(request, position_id, next_code):
    pos = Position.objects.get(id=position_id)
    
    if pos.status_code == 1 and next_code == 3:
        pos.status_code = 3
    elif pos.status_code == 1 and next_code == 4:
        pos.status_code = 4
        pos.fu_sent = False
    elif pos.status_code == 1 and next_code == 31:
        pos.status_code = 31
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 1 and next_code == 32:
        pos.status_code = 32
        pos.fu_sent = False

    elif pos.status_code == 11 and next_code == 4:
        pos.status_code = 4
        pos.fu_sent = False
        pos.ty_sent = False
    elif pos.status_code == 11 and next_code == 14:
        pos.status_code = 14
        pos.fu_sent = False
        pos.assignment_done = False
    elif pos.status_code == 11 and next_code == 21:
        pos.status_code = 21
    elif pos.status_code == 11 and next_code == 33:
        pos.status_code = 33
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 11 and next_code == 34:
        pos.status_code = 34
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    
    elif pos.status_code == 2 and next_code == 1:
        pos.status_code = 1
        pos.fu_sent = True
    elif pos.status_code == 3 and next_code == 1:
        pos.status_code = 1
        pos.assignment_done = True
    elif pos.status_code == 4 and next_code == 12:
        pos.status_code = 12
        pos.fu_sent = False
        pos.ty_sent = False
    elif pos.status_code == 4 and next_code == 21:
        pos.status_code = 21
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 12 and next_code == 11:
        pos.status_code = 11
        pos.ty_sent = True
    elif pos.status_code == 13 and next_code == 11:
        pos.status_code = 11
        pos.fu_sent = True
    elif pos.status_code == 14 and next_code == 11:
        pos.status_code = 11
        pos.assignment_done = True
    
    elif pos.status_code == 21 and next_code == 22:
        pos.status_code = 22
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 21 and next_code == 23:
        pos.status_code = 23
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 22 and next_code == 4:
        pos.status_code = 4
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 22 and next_code == 21:
        pos.status_code = 21
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False

    elif pos.status_code == 31 and next_code == 4:
        pos.status_code = 4
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 32 and next_code == 4:
        pos.status_code = 4
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 33 and next_code == 4:
        pos.status_code = 4
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 33 and next_code == 21:
        pos.status_code = 21
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 34 and next_code == 4:
        pos.status_code = 4
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    elif pos.status_code == 34 and next_code == 21:
        pos.status_code = 21
        pos.fu_sent = False
        pos.assignment_done = False
        pos.ty_sent = False
    
    pos.save()
    # TODO django's updated_at auto is 7 hours ahead???
    return redirect('/dashboard')
    
    
    
    
def refresh_followups():
    # look at all positions in waiting
    
    # applied, followup not sent, updated_at is more than X days ago -> change status from 1 to 2
    
    # interviewed, followup not sent, updated_at is more than X days ago -> change status from 11 to 13
    return