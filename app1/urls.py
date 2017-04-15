from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /app1/
    url(r'^$', views.index, name='index'),
    url(r'^home$',views.apphome, name='apphome'),
    url(r'^contact$',views.contact, name='contact'),
    url(r'^Word\ compare$',views.compare_view, name='wordpop'),
    url(r'^location$', views.location_view, name='location_url'),
    url(r'^Language\ Compare$', views.langpop, name='langpop'),
]
