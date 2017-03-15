from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from hellocode.models import CoderProfile


@login_required
def me(request):
    """Renders the home page"""
    user = request.user

    data = dict()
    data['skills'] = Skill.objects.filter(user=user)
    data['coder'] = CoderProfile.objects.get(user=user)
    
    return render(request, 'users/me.html', data)