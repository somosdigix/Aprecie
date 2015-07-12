from django.conf.urls import include, url
from Reconhecimentos import views

urlpatterns = [
    url(r'^reconhecer/$', views.reconhecer, name="reconhecer"),
    url(r'^ultimos/$', views.ultimos_reconhecimentos, name="ultimos_reconhecimentos"),
    url(r'^funcionario/$', views.reconhecimentos_do_funcionario, name="reconhecimentos_do_funcionario"),
    url(r'^por_reconhecedor/$', views.reconhecimentos_por_reconhecedor, name="reconhecimentos_por_reconhecedor"),
]