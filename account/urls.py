from django.conf.urls import patterns, url
from account.views import logout_view, register, success
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete, login
from django.http import HttpResponseRedirect, HttpResponse


urlpatterns = patterns('account.views',
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^registration/$', register, name='register'),
    url(r'^success/$', success, name='success'),
    )