from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Question, Response

from taggit.models import Tag


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ('title', 'body_md', 'tags')
    template_name = "questions/question_form.html"
    form = ModelFormMixin

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreateView, self).form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ('title', 'body_md', 'tags')
    template_name = "questions/question_form.html"

    def get_object(self, *args, **kwargs):
        obj = super(QuestionUpdateView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied()
        return obj


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['responses'] = Response.objects.filter(question__slug=slug)
        return context

    template_name = "questions/question_detail.html"


# class TagListView(ListView):
#     model = Tag
#     template_name = "questions/tag_list.html"


# class TagQuestionsList(ListView):
#     def get_queryset(self):
#         slug = self.kwargs['slug']
#         return Question.objects.filter(tags__name=slug).order_by('-created')

#     template_name = "questions/tag_questions_list.html"


@login_required
def create_response(request):
    question = None
    if request.POST:
        r = Response()
        r.user = request.user
        question = Question.objects.get(id=request.POST.get('qid'))
        r.question = question
        r.body_md = request.POST.get('body')
        r.save()


    return redirect(question)

