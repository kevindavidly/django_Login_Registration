from django.db import models
import re
import bcrypt  

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# Create your models here.
class UserManager(models.Manager) :
    def reg_validator(self, postData) :
        errors = {}
        if len(postData["fname"]) < 2 :
            errors["first_name"] = "First name must be at least 2 characters"
        if len(postData["lname"]) < 2 :
            errors["last_name"] = "Last name must be at least 2 characters"
        if not EMAIL_REGEX.match(postData["email"]) :
            errors["email"] = "Invalid email address"
        if len(postData["password"]) < 8 :
            errors["password"] = "Password must be at least 8 characters"
        if postData["password"] != postData["c_password"] :
            errors["password"] = "Passwords do not match"
        return errors
    def login_validator(self, postData) :
        errors = {}
        matching_emails = User.objects.filter(email=postData["email"])
        if len(matching_emails) < 1 :
            errors["email_log"] = "No such email exists!"
        matches = 0
        for x in matching_emails :
            if bcrypt.checkpw(postData["password"].encode(), x.password.encode()) :
                matches += 1
        if matches == 0 :
            errors["password_log"] = "Password does not match!"
        return errors

class User(models.Model) :
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

