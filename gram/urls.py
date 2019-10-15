from django.conf.urls import url
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^myaccount/$', views.prof, name='myaccount'),
    url(r'^myaccount/edit/$', views.edit, name='edit'),
]
