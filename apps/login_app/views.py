from django.shortcuts import render, redirect 
from django.contrib import messages
from .models import *
import bcrypt 

# Create your views here.
def index(request) :
    request.session["log_status"] = False   #Set default val so users cannot access success
    return render(request, "login_app/index.html")

def register_process(request) :
    print ("Processed")
    if request.method == "POST" :
        errors = User.objects.reg_validator(request.POST)   #pass POST data to registration validator 
        print (errors)
        if len(errors) > 0 :
            for key, value in errors.items() :
                messages.error(request, value, extra_tags=key)
            return redirect("/")
        else :
            pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST["fname"], last_name=request.POST["lname"], email=request.POST["email"], password=pw_hash)
            return redirect("/")
        
def login(request) :
    print("Logged")
    if request.method == "POST" :
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0 :
            for key, value in errors.items() :
                messages.error(request, value, extra_tags=key)
            return redirect("/")
        else :
            messages.success(request, "Successfully logged in!", extra_tags="success")
            user = User.objects.get(email=request.POST["email"])
            request.session["log_status"] = True
            request.session['id'] = user.id
            request.session['first_name'] = user.first_name
            return redirect ("/success")

def success(request) :
    if not request.session["log_status"] : 
        messages.warning(request, "Bitch don't do that!", extra_tags="warning")
        return redirect("/")
    else :
        return render(request, "login_app/success.html")

def logout(request) :
    request.session["log_status"] = False 
    return redirect("/")
        