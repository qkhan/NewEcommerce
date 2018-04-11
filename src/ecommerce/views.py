from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from .forms import ContactForm

def home_page(request):
    context = {
        "title": "Hello World!",
        "content": "This is content for the home page"
    }
    return render(request, 'home.html', context)

def about_page(request):
    context = {
        "title": "About Page",
        "content": "This is content for the About page",
    }
    return render(request, 'about.html', context)

def contact_page(request):

    contact_form = ContactForm(request.POST or None)

    context = {
        "title": "Contact",
        "content": "This is content for the Contact page",
        "form" : contact_form,
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission."})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, 'contact.html', context)
