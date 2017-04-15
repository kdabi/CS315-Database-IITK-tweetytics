from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /app1/
    url(r'^$', views.index, name='index'),
    url(r'^home$',views.apphome, name='apphome'),
    url(r'^contact$',views.contact, name='contact'),
    url(r'^word_compare$',views.wordpop, name='wordpop'),
]
