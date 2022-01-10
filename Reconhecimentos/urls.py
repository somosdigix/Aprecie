from django.conf.urls import include, url
from Reconhecimentos import views

urlpatterns = [
    url(r'^reconhecer/$', views.reconhecer, name="reconhecer"),
    url(r'^ultimos/$', views.ultimos_reconhecimentos, name="ultimos_reconhecimentos"),
    url(r'^colaborador/([0-9]+)$', views.reconhecimentos_do_colaborador, name="reconhecimentos_do_colaborador"),
    url(r'^por_reconhecedor/([0-9]+)$', views.reconhecimentos_por_reconhecedor, name="reconhecimentos_por_reconhecedor"),
    url(r'^todos/([0-9]+)$', views.todas_as_apreciacoes, name="todas_as_apreciacoes"),
    url(r'^definir_ciclo/$', views.definir_ciclo, name="definir_ciclo"),
    url(r'^alterar_ciclo/$', views.alterar_ciclo, name="alterar_ciclo"),
    url(r'^obter_ciclos/$', views.obter_ciclos, name="obter_ciclos"),
    url(r'^([0-9]+)/([0-9]+)$', views.reconhecimentos_por_pilar, name="reconhecimentos_por_pilar"),
]
