from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from website import views as wv
from users import views as uv
from questions import views as qv


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # overrides allauth's logout to enable single click logout.
    url(r'^users/logout/$', logout, {'next_page': '/'}),
    url(r'^users/', include('allauth.urls')),
    url(r'^dashboard', uv.dashboard, name='dashboard'),
    url(r'^profile/create', uv.ProfileCreateView.as_view(),
        name='create_profile'),
    url(r'^@(?P<slug>[-\w]+)/update', uv.ProfileUpdateView.as_view(),
        name='update_profile'),
    url(r'^@(?P<slug>[-\w]+)', uv.public_profile, name='public_profile'),
    url(r'^t/(?P<slug>[-\w]+)$', qv.tag_questions_list, name="tags_tag"),
    url(r'^q/', include('questions.urls')),
    url(r'^ask$', qv.QuestionCreateView.as_view(), name="ask"),
    url(r'^questions$', qv.questions_list, name="questions"),
    url(r'^create_response$', qv.create_response, name="create_response"),
    url(r'^slack2devolio$', qv.slack2devolio, name="slack2devolio"),
    url(r'^$', wv.index, name='ws_index')
]
