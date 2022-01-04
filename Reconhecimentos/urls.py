from django.conf.urls import include, url
from Reconhecimentos import views

urlpatterns = [
    url(r'^reconhecer/$', views.reconhecer, name="reconhecer"),
    url(r'^ultimos/$', views.ultimos_reconhecimentos, name="ultimos_reconhecimentos"),
    url(r'^colaborador/([0-9]+)$', views.reconhecimentos_do_colaborador, name="reconhecimentos_do_colaborador"),
    url(r'^por_reconhecedor/([0-9]+)$', views.reconhecimentos_por_reconhecedor, name="reconhecimentos_por_reconhecedor"),
    url(r'^todos/([0-9]+)$', views.todas_as_apreciacoes, name="todas_as_apreciacoes"),
    url(r'^ranking/$', views.contar_reconhecimentos, name="contar_reconhecimentos"),
    url(r'^([0-9]+)/([0-9]+)$', views.reconhecimentos_por_pilar, name="reconhecimentos_por_pilar"),
    url(r'^ranking_de_pilares/([0-9]+)$', views.ranking_de_pilares, name="ranking_de_pilares"),
    url(r'^ranking_por_periodo/$', views.ranking_por_periodo, name="ranking_por_periodo")
]