from django.shortcuts import render, redirect
from django.contrib import messages
from main.forms import *


# Create your views here.

def home(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            messages.success(request, "Your message has been sent successfully!")
            # return redirect('/')  # ریدایرکت برای جلوگیری از ارسال مجدد فرم
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
