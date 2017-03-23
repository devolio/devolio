from django.shortcuts import render
from questions.models import Question

def index(request):
    """Renders the home page"""
    questions = Question.objects.all()
    return render(request, 'website/index.html', {'questions':questions})
