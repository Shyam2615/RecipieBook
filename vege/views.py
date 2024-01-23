from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

@login_required(login_url='/login/')
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
    
        recipe.objects.create(
            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_image = recipe_image,
        )

        return redirect('/')
    
    queryset = recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search'))
        #__icontains method is used to check whether the letters enetred are available or not

    context={'recipes': queryset}
    return render(request, "recipes.html", context)

@login_required(login_url='/login/')
def delete_recipe(request, id):
    queryset = recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/')

@login_required(login_url='/login/')
def update_recipe(request, id):
    query_set = recipe.objects.get(id = id)
    context={'recipe': query_set}
    if request.method == 'POST':
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        query_set.recipe_name = recipe_name
        query_set.recipe_description = recipe_description
        if recipe_image:
            query_set.recipe_image = recipe_image

        query_set.save()

        return redirect('/')
    return render(request, "update_recipe.html", context)

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not User.objects.filter(username = email).exists():
            messages.info(request, 'Invalid username')
            return redirect('/login/')
        
        user = authenticate(username = email, password = password)
        print(user)

        if user is None:
            messages.info(request, 'Invalid password')
            return redirect('/login/')
        else:
            login(request , user)
            return redirect('/')



    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = email)
        if user.exists():
            messages.info(request, 'User already exists')
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = email,
        )
        # In User model already the first_name last_name username are created in django

        user.set_password(password)
        # we need to use this for password storage bcz if we directly create by objects.create it will store only string but the password needs to be hashed and salted for security thats y we use this method
        user.save()
        messages.info(request, 'Account created succesfully')

        # Code to send email
        subject = "Welcome to Recipe Book"
        message = f"Hii {first_name} we are glad to see you here Thank-you for registering in Recipe_book"
        email_from = settings.EMAIL_HOST_USER
        recipent_email = [email]

        send_mail(subject, message, email_from, recipent_email)
        return redirect('/')


    return render(request, "register.html")