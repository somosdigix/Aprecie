from django.conf.urls import include, url
from Reconhecimentos import views

urlpatterns = [
    url(r'^pilares/$', views.todos_os_pilares_e_colaboradores, name="todos_os_pilares_e_colaboradores"),
    url(r'^reconhecer/$', views.reconhecer, name="reconhecer"),
    url(r'^ultimos/$', views.ultimos_reconhecimentos, name="ultimos_reconhecimentos"),
    url(r'^colaborador/([0-9]+)$', views.reconhecimentos_do_colaborador, name="reconhecimentos_do_colaborador"),
    url(r'^por_reconhecedor/([0-9]+)$', views.reconhecimentos_por_reconhecedor, name="reconhecimentos_por_reconhecedor"),
    url(r'^todos/([0-9]+)$', views.todas_as_apreciacoes, name="todas_as_apreciacoes"),
    url(r'^definir_ciclo/$', views.definir_ciclo, name="definir_ciclo"),
    url(r'^alterar_ciclo/$', views.alterar_ciclo, name="alterar_ciclo"),
    url(r'^obter_informacoes_ciclo_atual/$', views.obter_informacoes_ciclo_atual, name="obter_informacoes_ciclo_atual"),
    url(r'^ranking/$', views.contar_reconhecimentos, name="contar_reconhecimentos"),
    url(r'^([0-9]+)/([0-9]+)$', views.reconhecimentos_por_pilar, name="reconhecimentos_por_pilar"),
    url(r'^ciclos_passados/$', views.ciclos_passados, name="ciclos_passados"),
    url(r'^historico_alteracoes/$', views.historico_alteracoes, name="historico_alteracoes"),
    url(r'^ranking_por_periodo/$', views.ranking_por_periodo, name="ranking_por_periodo")
]