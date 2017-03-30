from django.conf.urls import url, include
from questions import views as qv


urlpatterns = [
    url(r'^ask$', qv.QuestionCreateView.as_view(), name="ask"),
    url(r'^questions$', qv.questions_list, name="questions"),
    url(r'^response$', qv.create_response, name="response"),
    url(r'^(?P<slug>[-\w]+)/edit$', qv.QuestionUpdateView.as_view(), name="q_edit"),
    url(r'^(?P<slug>[-\w]+)$', qv.QuestionDetailView.as_view(), name="q_detail")

]
