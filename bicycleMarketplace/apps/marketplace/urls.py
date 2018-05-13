from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout),
    url(r'^browse$', views.browse, name='browse'),
    url(r'^bikes$', views.bikes, name='bikes'),
    url(r'^bikes/(?P<bikeId>\d+)$', views.viewbike, name='view'),
    url(r'^createbike$', views.createbike, name='create'),
    url(r'^bikes/update/(?P<bikeId>\d+)$', views.updatebike, name='update'),
    url(r'^bikes/delete(?P<bikeId>\d+)$', views.deletebike, name='delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)