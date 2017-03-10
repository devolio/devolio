from django.shortcuts import render

def index(request):
    return render(request, 'hellocode/index.html')

def new_dev(request):
    return render(request, 'hellocode/new_dev.html')

def proj_suggestions(request):
    return render(request, 'hellocode/proj_suggestions.html')