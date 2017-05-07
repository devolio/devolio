from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin
from .models import Profile
from questions.models import Question
from questions.views import paginate


@login_required
def dashboard(request):
    """Renders the home page"""
    user = request.user

    context = dict()
    context['questions'] = Question.objects.filter(user=user)
    context['responded_to_qs'] = Question.objects.filter(response__user=user).distinct()

    return render(request, 'users/dashboard.html', context)


def public_profile(request, slug):
    user = User.objects.get(username=slug)
    questions = paginate(
        Question.objects.filter(user__username=slug).order_by('-created'),
        5, request)

    return render(request, 'users/public_profile.html', {
        'user': user,
        'questions': questions
        })


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ('summary', 'good_skills', 'learning_skills',
              'code_url', 'website')
    template_name = "users/profile_form.html"
    form = ModelFormMixin

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        try:
            slug = request.user.profile.slug
            return redirect('update_profile', slug)
        except:
            pass
        return super(ProfileCreateView, self).dispatch(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ('summary', 'good_skills', 'learning_skills',
              'code_url', 'website')
    template_name = "users/profile_form.html"

    def get_object(self, *args, **kwargs):
        obj = super(ProfileUpdateView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied()
        return obj

