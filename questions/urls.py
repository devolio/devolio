from django.conf.urls import url, include
from questions import views as qv


urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/edit$', qv.QuestionUpdateView.as_view()),
    url(r'^(?P<slug>[-\w]+)$', qv.QuestionDetailView.as_view()),
    url(r'^ask$', qv.QuestionCreateView.as_view()),
    url(r'^tags/(?P<slug>[-\w]+)$', qv.TagQuestionsList.as_view()),
    url(r'^tags/$', qv.TagListView.as_view())
]
