from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
    context = {
        "title": "Hello World!",
        "content": "This is content for the home page"
    }
    return render(request, 'views/home.html', context)

def about_page(request):
    context = {
        "title": "About Page",
        "content": "This is content for the About page",
    }
    return render(request, 'views/about.html', context)

def contact_page(request):

    contact_form = ContactForm(request.POST or None)

    context = {
        "title": "Contact",
        "content": "This is content for the Contact page",
        "form" : contact_form,
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, 'views/contact.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)

    context = {
        "form": form
    }

    if form.is_valid():
        print (form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print ("User: ", user)
            print ("isAuhthenticated: ", request.user.is_authenticated())
            login(request, user)
            return redirect("/login")
        else:
            print("Error")

    return render(request, "auth/login.html", context)


User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username, password, email)
        print ("New User: ", new_user)
    return render(request, "auth/register.html", context)
