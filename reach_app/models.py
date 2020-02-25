from django.db import models
import re
import bcrypt
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        
        # FN more than 2
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"

        # LN more than 2
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        
        # Email Valid
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"

        # Unique email
        given_email = postData['email']
        temp = User.objects.filter(email=given_email)
        if len(temp) != 0:
            errors['email'] = 'Invalid email address'
            
        # PW matches
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Passwords don't match"

        # PW longer than 8
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['login_email'])
        # If no matching user found
        if len(user) != 1:
            errors['login_email']='Invalid email address or password.'
        # If matching user found, but...
        else:
            # If password check returns false
            if bcrypt.checkpw(postData['login_password'].encode(), user[0].password.encode()) == False:
                errors['login_email']='Invalid email address or password./'
        
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    # positions = list of associated positions
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class CompanyManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        
        # Company Link format
        if len(postData['company_info']) > 0:
            if postData['company_info'].startswith('http://') == False and postData['company_info'].startswith('https://') == False:
                errors['company_info'] = "Please enter the entire company URL"
        
        return errors
        
class Company(models.Model):
    name=models.CharField(max_length=255)
    info=models.TextField(default="")
    # positions = list of associated positions
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CompanyManager()
    
class Contact(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    # positions = list of associated positions
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class PositionManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        
        # Title more than 2
        if len(postData['title']) < 2:
            errors['title'] = "Job Title must be at least 2 characters"

        # Location more than 2
        if len(postData['location']) < 2:
            errors['location'] = "Location must be at least 2 characters"
            
        # Salary format
        try: 
            if int(postData['salary']) > 0:
                pass
        except: 
            errors['salary'] = "Please enter the salary in the correct format. (ex: $500,000 should be entered as 500000)"
            
        # Link format
        if postData['posting'].startswith('http://') == False and postData['posting'].startswith('https://') == False:
            errors['posting'] = "Please enter the entire job post URL"

        # Position Uniqueness with Given Company
        same_titles = Position.objects.filter(title=postData['title'])
        if len(same_titles) != 0: 
            for position in same_titles:
                if position.company.name == postData['company_name']:
                    errors['title'] = "Position already exists"
            
        return errors

class Position(models.Model):
    user=models.ForeignKey(User, related_name="positions", on_delete = models.CASCADE)
    title=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    salary=models.IntegerField(blank=True, null=True)
    posting=models.TextField()
    company=models.ForeignKey(Company, blank=True, null=True, related_name="positions", on_delete = models.CASCADE)
    contact=models.ForeignKey(Contact, blank=True, null=True, related_name="positions", on_delete = models.CASCADE)
    # limit to ~300 chars?
    note=models.TextField(default="None")
    fu_sent=models.BooleanField(default=False)
    assignment_done=models.BooleanField(default=False)
    ty_sent=models.BooleanField(default=False)
    
    # TODO come back and change max value
    status_code=models.IntegerField(
        default=1,
        validators=[MaxValueValidator(40), MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PositionManager()