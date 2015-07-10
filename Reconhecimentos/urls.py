from django.conf.urls import include, url
from Reconhecimentos import views

urlpatterns = [
    url(r'^reconhecer/$', views.reconhecer, name="reconhecer"),
    url(r'^funcionario/$', views.reconhecimentos_do_funcionario, name="reconhecimentos_do_funcionario"),
]