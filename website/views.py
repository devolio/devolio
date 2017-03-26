from django.shortcuts import render, redirect
from django.template.response import SimpleTemplateResponse


def index(request):

    # if the user is not logged in, show main page
    if request.user.is_authenticated:
        return redirect('questions')

    return SimpleTemplateResponse('website/index.html')
