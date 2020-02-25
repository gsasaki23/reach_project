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


class Company(models.Model):
    name=models.CharField(max_length=255)
    info=models.TextField()
    # positions = list of associated positions
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Contact(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    # positions = list of associated positions
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Position(models.Model):
    user=models.ForeignKey(User, related_name="positions", on_delete = models.CASCADE)
    title=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    salary=models.IntegerField(blank=True, null=True)
    posting=models.TextField()
    company=models.ForeignKey(Company, blank=True, null=True, related_name="positions", on_delete = models.CASCADE)
    contact=models.ForeignKey(Contact, blank=True, null=True, related_name="positions", on_delete = models.CASCADE)
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