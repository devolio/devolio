from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from questions.models import Question


@login_required
def me(request):
    """Renders the home page"""
    user = request.user

    data = dict()
    data['questions'] = Question.objects.filter(user=user)
    
    return render(request, 'users/me.html', data)