from django.shortcuts import render, redirect
from .models import Message
from django.contrib import messages

def store_message(request):
    if request.method == "POST":
        user_name = request.POST["user_name"]
        user_email = request.POST["user_email"]
        user_message = request.POST["user_message"]

        contact = Message(user_name=user_name, user_email=user_email,user_message=user_message)
        contact.save()

        messages.success(request, 'Your request has been submitted, an admin will get back to you soon')
        return redirect('/')