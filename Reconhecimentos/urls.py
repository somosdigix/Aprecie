from django.conf.urls import include, url
from Reconhecimentos import views

urlpatterns = [
    url(r'^reconhecer/$', views.reconhecer, name="reconhecer"),
    url(r'^ultimos/$', views.ultimos_reconhecimentos, name="ultimos_reconhecimentos"),
    url(r'^colaborador/([0-9]+)$', views.reconhecimentos_do_colaborador, name="reconhecimentos_do_colaborador"),
    url(r'^por_reconhecedor/([0-9]+)$', views.reconhecimentos_por_reconhecedor, name="reconhecimentos_por_reconhecedor"),
    url(r'^([0-9]+)/([0-9]+)$', views.reconhecimentos_por_valor, name="reconhecimentos_por_valor"),
]