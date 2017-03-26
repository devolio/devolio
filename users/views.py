from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from questions.models import Question
from questions.views import paginate
from .forms import ProfileForm


@login_required
def me(request):
    """Renders the home page"""
    user = request.user

    context = dict()
    context['questions'] = Question.objects.filter(user=user)
    
    return render(request, 'users/me.html', context)


def public_user(request, slug):
    user = User.objects.get(username=slug)
    questions = paginate(
        Question.objects.filter(user__username=slug).order_by('-created'),
        5, request)

    return render(request, 'users/public_user.html',
        {
        'user': user,
        'questions': questions
        })


@login_required
def create_profile(request):
    form = ProfileForm

    if request.method == 'POST':
        f = ProfileForm(request.POST)
        if f.is_valid():

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            summary = request.POST.get('summary')
            good_skills = request.POST.get('good_skills')
            learning_skills = request.POST.get('learning_skills')
            slack_handle = request.POST.get('slack_handle')
            code_url = request.POST.get('code_url')
            website = request.POST.get('website')

            p = Profile(
                user=request.user,
                summary=summary,
                slack_handle=slack_handle,
                code_url=code_url,
                website=website)

            p.save()

    return render(request, 'users/profile_form.html', {'form': form})


