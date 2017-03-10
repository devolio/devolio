from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^start$', new_dev, name='hc_dew_dev'),
    url(r'^suggestions$', proj_suggestions, name='hc_proj_suggestions'),
    url(r'^$', index, name='hc_index')
]
