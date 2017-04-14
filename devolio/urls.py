from django.conf.urls import url, include
from django.contrib import admin
from website import views as wv
from users import views as uv
from questions import views as qv


urlpatterns = [
    url(r'^admin/', admin.site.urls),
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
    url(r'^new_response$', qv.new_reply, name="new_reply"),
    url(r'^$', wv.index, name='ws_index')
]
