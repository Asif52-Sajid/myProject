from django.shortcuts import render
from products.models import Product
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
def base(request):
    return render(request,'base.html')


def home(request):
    return render(request, 'components/home.html')
def product(request):
    products = Product.objects.all()
    return render(request, 'components/product.html', {"products":products, })

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')  # Corrected to match 'password2' from the form

        # Basic validations
        if not uname or not email or not pw1 or not pw2:
            messages.error(request, "All fields are required.")
            return render(request, 'components/register.html')

        if pw1 != pw2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'components/register.html')

        # Check if the username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'components/register.html')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'components/register.html')

        # Create the user
        try:
            my_user = User.objects.create_user(username=uname, email=email, password=pw1)
            my_user.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')  # Replace 'login' with the name of your login URL
        except Exception as e:
            messages.error(request, "An error occurred while creating the account.")
            return render(request, 'components/register.html')

    return render(request, 'components/register.html')

def LOGIN(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or password is incorrect!")

    return render(request, 'components/login.html')


def LOGOUT(request):
    logout(request)
    return redirect("home")