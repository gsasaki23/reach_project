from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime
from dateutil.relativedelta import relativedelta


# GET for Index page
def index(request):
    return render(request, 'index.html')

# GET for Dashboard page
def dashboard(request):
    try:
        refresh_followups(request)
        
        
        code_21 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 21)
        code_22 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 22)
        code_23 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 23)
        reached_positions = code_21 | code_22 | code_23
        reached_positions.order_by("status_code")
        
        code_2 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 2)
        code_3 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 3)
        code_4 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 4)
        code_12 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 12)
        code_13 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 13)
        code_14 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 14)
        todo_positions = code_2 | code_3 | code_4 | code_12 | code_13 | code_14
        todo_positions.order_by("updated_at")
        
        code_1 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 1)
        code_11 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 11)
        waiting_positions = code_1 | code_11
        waiting_positions.order_by("updated_at")
        
        code_31 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 31)
        code_32 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 32)
        code_33 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 33)
        code_34 = User.objects.get(id=request.session['user_id']).positions.filter(status_code = 34)
        obsolete_positions = code_31 | code_32 | code_33 | code_34
        obsolete_positions.order_by("updated_at")
        
                
        context = {
            "current_user": User.objects.get(id=request.session['user_id']),
            "total_positions": len(User.objects.get(id=request.session['user_id']).positions.all()),
            "today_date": datetime.now().date(),
            # Area 1
            "reached_positions": reached_positions,
            "reached_positions_count": len(reached_positions),
            # Area 2
            "todo_positions": todo_positions,
            "todo_positions_count": len(todo_positions),
            # Area 3
            "waiting_positions": waiting_positions,
            "waiting_positions_count": len(waiting_positions),
            # Area 4
            "obsolete_positions": obsolete_positions,
            "obsolete_positions_count": len(obsolete_positions),
        }
        return render(request, 'dashboard.html', context)
    except KeyError:
        return redirect('/')

# GET for New page
def new(request):
    try:
        context = {
            "current_user": User.objects.get(id=request.session['user_id']),
            "companies": Company.objects.all(),
        }
        return render(request, 'new.html', context)
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
        request.session['user_id'] = User.objects.last().id
        return redirect('/dashboard')

# POST for login, route to dashboard if success
def attempt_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        request.session['user_id'] = User.objects.get(email=request.POST['login_email']).id
        return redirect('/dashboard')

# POST for logging out, clearing session
def logout(request):
    del request.session['user_id']
    return redirect('/')

# POST for new position, route to dashboard if success
def attempt_position(request):
    # Validate Company Data
    errors = Company.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    else:
        # If company doesn't exist, create new, otherwise get existing object    
        if len(Company.objects.filter(name=request.POST["company_name"])) == 0:
            Company.objects.create(
                name=request.POST["company_name"],
            )
            add_company = "existing"
        else:
            add_company = Company.objects.get(name=request.POST["company_name"])
    
    # If contact was given
    if request.POST["contact_have"] == "true":
        # Validate Contact Data
        errors = Contact.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new')
        elif request.POST["contact_name"] == "":
            add_contact = None
        else:
            Contact.objects.create(
                full_name=request.POST["contact_name"],
                phone=request.POST["contact_phone"],
                email=request.POST["contact_email"],
            )
            add_contact = Contact.objects.last()
    else:
        add_contact = None
    
    # Validate Position Data
    errors = Position.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    else:
        if add_company == "existing":
            add_company = Company.objects.last()
        # Creates new position
        Position.objects.create(
            user=User.objects.get(id=request.session['user_id']),
            title=request.POST["title"],
            location=request.POST["location"],
            salary=request.POST["salary"],
            posting=request.POST["posting"],
            note=request.POST["note"],
            company=add_company,
            contact=add_contact,
        )
        return redirect('/dashboard')

# POST for new position, route to dashboard if success
def edit_position(request, position_id):
    pos = Position.objects.get(id=position_id)

    pos.title=request.POST["title"]
    pos.location=request.POST["location"] 
    pos.salary=request.POST["salary"]
    pos.posting=request.POST["posting"]
    pos.note=request.POST["note"]
    
    # TODO missing validation on new company create?
    # If new company:
    if len(Company.objects.filter(name=request.POST["company_name"])) == 0:
        if request.POST["company_info"] == "":
            temp_info = "" 
        else:
            temp_info = request.POST["company_info"]
        
        Company.objects.create(
            name=request.POST["company_name"],
            info=temp_info,
        )
        add_company = Company.objects.last()
    # If existing company:
    else:
        add_company = Company.objects.get(name=request.POST["company_name"])
        # If info is a new link, overwrite
        if add_company.info != request.POST["company_info"]:
            add_company.info = request.POST["company_info"]
            add_company.save()
    
    # If new contact (i.e. position doesnt have contact yet):
    if request.POST['contact_have'] == "true" and pos.contact == None:
        # Validate Contact Data
        errors = Contact.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit')
        else:
            Contact.objects.create(
                full_name=request.POST["contact_name"],
                phone=request.POST["contact_phone"],
                email=request.POST["contact_email"],
            )
            pos.contact = Contact.objects.last()
        
    # If existing contact:
    elif request.POST['contact_have'] == "true" and pos.contact != None:
        # Validate Contact Data
        errors = Contact.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{pos.id}')
        else:
            pos.contact.full_name = request.POST['contact_name']
            pos.contact.phone = request.POST['contact_phone']
            pos.contact.email = request.POST['contact_email']
            pos.contact.save()
    
    pos.company=add_company
    pos.save()
    return redirect('/dashboard')

# POST for deleting position, route to dashboard
def delete_position(request, position_id):
    pos = Position.objects.get(id=position_id)
    pos.delete()
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
    elif pos.status_code == 4 and next_code == 31:
        pos.status_code = 31
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
    
    pos.save()
    # TODO django's updated_at auto is 7 hours ahead???
    return redirect('/dashboard')
    
# Adds necessary followups to waiting positions    
def refresh_followups(request):
    user_followup_setting = 7
    today_minus_days = datetime.now() + relativedelta(days=-user_followup_setting)

    for position in User.objects.get(id=request.session['user_id']).positions.filter(status_code=1):
        if (position.updated_at.date() >= today_minus_days.date() and position.fu_sent == False):
            position.status_code == 2
            position.save()
    
    for position in User.objects.get(id=request.session['user_id']).positions.filter(status_code=11):
        if (position.updated_at.date() >= today_minus_days.date() and position.fu_sent == False):
            position.status_code == 13
            position.save()
    return