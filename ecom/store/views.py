from django.shortcuts import render,redirect
from .models import Product, Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products': products})

def about(request):
    return render(request,'about.html',{})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("you are logged in"))
            return redirect("home")
        else:
            messages.success(request,("there was some error"))
            return redirect("login")
    else:       
        
        return render(request,"login.html",{})


def logout_user(request):
    logout(request)
    messages.success(request,("you have been logged out"))
    return redirect("home")

def register_user(request):
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,f"Account got created for {username}!")
            return redirect('update_info')
    else:
        form = SignUpForm()
    return render(request,'register.html',{'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id= request.user.id)
        user_form  = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request,current_user)
            messages.success(request,"user has been update")
            return redirect("home")
        
        return render(request,'update_user.html',{"user_form":user_form})
    else:
        messages.success(request,"you must be logged in to access the page")
        return redirect("home")
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id= request.user.id)
        form  = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save() 
            messages.success(request,"user info has been update")
            return redirect("home")
        
        return render(request,'update_info.html',{"form":form})
    else:
        messages.success(request,"you must be logged in to access the page")
        return redirect("home")
    
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            #do stuff
            form  = ChangePasswordForm(current_user,request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request,"user password has been updated")
                #login(request,current_user)
                return redirect("login")
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect("update_password")
                
                
        else:
            form = ChangePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request,"you must be logged in to access the page")
        return redirect("home")
            
            
        
    
    

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product': product})

def category(request,cat):
    #replacing hyphons with spaces
    cat = cat.replace('-', ' ')
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        categories = Category.objects.all()
        return render(request,"category.html",{"products":products, "category":category, "categories":categories})
        
    except:
        messages.success(request,("that category doesnt exists"))
        return redirect('home')
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request,"category_summary.html",{'categories':categories})
    