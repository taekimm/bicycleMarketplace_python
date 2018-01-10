from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^browse$', views.browse, name='browse'),
    url(r'^bikes$', views.bikes, name='bikes'),
    url(r'^createbike$', views.createbike, name='create'),
    url(r'^updatebike$', views.updatebike, name='update'),
    url(r'^deletebike$', views.deletebike, name='delete'),
]