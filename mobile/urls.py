from django.conf.urls.defaults import *
from django.contrib.auth.views import login

from fereol.settings import PROJECT_PATH

import os

urlpatterns = patterns('',
    #MAIN PAGE
	url('login/$', login, {'template_name': 'mobile/login.html'}, 'user-login'),
    url('^$', 'fereol.mobile.views.main_page', name='main-page'),
    url(r'^nomobile/$', 'fereol.mobile.views.noMobile', name = 'no-mobile'),
	url(r'enrollment/$', 'fereol.mobile.views.studentSubjectList', name = 'student-enrollment'),
    url(r'^(?P<cat>[\w\-_]+)/$', 'news.views.latest_news', name='latest_news'),
	(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}),
)