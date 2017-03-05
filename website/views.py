from django.shortcuts import render

def index(request):
    """Renders the home page"""
    return render(request, 'website/index.html')
