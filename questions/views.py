from django.shortcuts import render
from .models import Question
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from taggit.models import Tag


class QuestionCreateView(CreateView):
    model = Question
    fields = ('title', 'body_md', 'tags')
    template_name = "questions/question_form.html"


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ('title', 'body_md', 'tags')
    template_name = "questions/question_form.html"


class QuestionDetailView(DetailView):
    model = Question
    slug_field = 'slug'
    template_name = "questions/question_detail.html"


class TagListView(ListView):
    model = Tag
    template_name = "questions/tag_list.html"


class TagQuestionsList(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        return Question.objects.filter(tags__name=slug).order_by('-created')

    template_name = "questions/tag_questions_list.html"

