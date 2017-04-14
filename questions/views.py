from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Response

from taggit.models import Tag

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

from devolio.settings import firebase
from firebase import FIREBASE_JS_CONFIG


def send_to_firebase(reply):
    thread = "question-responses/{}".format(reply.question.id)
    firebase.database().child(thread).push({
                "body": reply.body_html,
                "user": reply.user.username,
                "user_id": reply.user.id,
                "reply_db_id": reply.id
        })


def paginate(qs, size, request):
    """takes a QS, size `request` and returns paginated data"""
    paginator = Paginator(qs, size)
    page = request.GET.get('page')

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)
    return qs


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
        context['firebase_config'] = json.dumps(FIREBASE_JS_CONFIG)
        return context

    template_name = "questions/question_detail.html"


def tag_questions_list(request, slug):
    return render(request, 'questions/questions_list.html',
        {
        'questions': Question.objects.filter(tags__name=slug).order_by('-created'),
        'tag_name': Tag.objects.get(slug=slug).name,
        'tags': Tag.objects.all().order_by('name'),
        })


@login_required
def new_reply(request):

    data = json.loads(request.body)
    print('this', len(data.get('body')))
    if not data.get('qid') or not data.get('body'):
        return HttpResponse('Some/all data is missing. Or server error.', status=400)

    r = Response()
    r.user = request.user
    question = Question.objects.get(id=data.get('qid'))
    r.question = question
    r.body_md = data.get('body')
    r.save()

    # push to firebase
    send_to_firebase(r)

    return HttpResponse('Response successful.')


def questions_list(request):
    return render(request, 'questions/questions_list.html',
        {
        'questions': paginate(Question.objects.all().order_by('-created'), 20, request),
        'tags': Tag.objects.all().order_by('name')
        })

