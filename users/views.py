from django.shortcuts import render

def me(request):
    """Renders the home page"""
    return render(request, 'users/me.html')
