from django.conf.urls import url
from questions import views as qv


urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/edit$', qv.QuestionUpdateView.as_view(), name="q_edit"),
    url(r'^(?P<slug>[-\w]+)$', qv.QuestionDetailView.as_view(), name="q_detail")

]
