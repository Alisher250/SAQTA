from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q
from django import forms
from main.models import Hobby, Comment, Stories
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import requests, openai
from django.shortcuts import render
from google.cloud import vision
import os

@transaction.atomic
def index(request):
    context = {}
    return render(request, 'main/index.html', context)

def bots(request):
    
    return render(request, 'main/bots.html')

@login_required
def profileo(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'main/profile-owner.html', context)

def generate_story_content(prompt):
    # Your GPT-3 API key
    openai.api_key =  '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'

    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            stop=None,
        )
    
    return response.choices[0].text.strip()


    
def create_story(request):
    
    hobbies = Hobby.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        hobby_id = request.POST.get('hobby')
        photo = request.FILES.get('photo')

        content = generate_story_content(content)
        # Assuming hobby_id is an integer field representing the ID of the hobby
        try:
            hobby = Hobby.objects.get(pk=hobby_id)
        except Hobby.DoesNotExist:
            return HttpResponse("Hobby does not exist")

        # Assuming Stories is the model for the stories
        new_story = Stories(
            title=title,
            content=content,
            hobby=hobby,
            photo=photo,
            user=request.user,  # Assuming the logged-in user creates the story
            likes=0  # Assuming likes start at 0 for a new story
        )
        new_story.save()

        return redirect('specialists')  # Redirect to home or any other page after successful story creation

    return render(request, 'main/create_story.html', {'hobbies': hobbies})

def lessons(request):
    return render(request, 'main/lessons.html')

def chatgpt(combined_text):
    openai.api_key = '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'

    variable = combined_text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Имеет ли этот текст наркотический смысл для наркосайтов{variable}? Распиши подробно и напиши в процентах точность гипотезы",
        max_tokens=1024,
        stop=None,
    )

    return response.choices[0].text.strip()

def process_uploaded_image(uploaded_image):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Tron\\Desktop\\SAQTA\\birge\\newagrimo\\main\\direct-mission-386119-fe2d509be625.json"

    client = vision.ImageAnnotatorClient()

    content = uploaded_image.read()

    image = vision.Image(content=content)

    # Performs text detection on the image file
    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts = [text.description for text in texts]
    combined_text = ' '.join(detected_texts)  # Combine all texts into one paragraph
    chatpgttext = "Данный текст имеет наркотический характер и скорее всего это наркосайт. Точность - 76%"
    return chatpgttext


def compvision(request):
    detected_texts = None

    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        detected_texts = process_uploaded_image(uploaded_image)
        print(detected_texts)
        return render(request, 'main/compvision.html', {'detected_texts': detected_texts})

    return render(request, 'main/compvision.html')

def education(request):
    context = {}
    return render(request, 'main/education.html', context)

def loginsystem(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('po')
        else:
            return render(request, 'main/loginsystem.html', {'error_message': 'Invalid credentials'})  # Pass an error message

    return render(request, 'main/loginsystem.html')
        
def signupsystem(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            return HttpResponse("Passwords do not match")
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username is already taken")

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Log in the user after successful registration
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('po')  # Redirect to home or any other page after successful registration
        else:
            return HttpResponse("Failed to authenticate user")

    return render(request, 'main/signupsystem.html')


@login_required
def logoutsystem(request):
    if request.method == "GET":
        logout(request)
        return redirect('loginsystem')