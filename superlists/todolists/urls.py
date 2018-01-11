from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'/To-Do$', views.index, name='To-Do_Lists')
]