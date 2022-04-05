from django.conf.urls import include, url
from Reconhecimentos.views import views, views_ranking, views_ciclo

urlpatterns = [
    url(r'^pilares/$', views.todos_os_pilares_e_colaboradores, name="todos_os_pilares_e_colaboradores"),
    url(r'^reconhecer/$', views.reconhecer, name="reconhecer"),
    url(r'^ultimos/$', views.ultimos_reconhecimentos, name="ultimos_reconhecimentos"),
    url(r'^colaborador/([0-9]+)$', views.reconhecimentos_do_colaborador, name="reconhecimentos_do_colaborador"),
    url(r'^por_reconhecedor/([0-9]+)$', views.reconhecimentos_por_reconhecedor, name="reconhecimentos_por_reconhecedor"),
    url(r'^todos/([0-9]+)$', views.todas_as_apreciacoes, name="todas_as_apreciacoes"),
    url(r'^([0-9]+)/([0-9]+)$', views.reconhecimentos_por_pilar, name="reconhecimentos_por_pilar"),
    
    url(r'^ranking/$', views_ranking.contar_reconhecimentos, name="contar_reconhecimentos"),
    url(r'^ranking_por_periodo/$', views_ranking.ranking_por_periodo, name="ranking_por_periodo"),
    
    url(r'^definir_ciclo/$', views_ciclo.definir_ciclo, name="definir_ciclo"),
    url(r'^alterar_ciclo/$', views_ciclo.alterar_ciclo, name="alterar_ciclo"),
    url(r'^obter_informacoes_ciclo_atual/$', views_ciclo.obter_informacoes_ciclo_atual, name="obter_informacoes_ciclo_atual"),
    url(r'^obter_informacoes_ciclo_futuro/$', views_ciclo.obter_informacoes_ciclo_futuro, name="obter_informacoes_ciclo_futuro"),
    url(r'^ciclos_passados/$', views_ciclo.ciclos_passados, name="ciclos_passados"),
    url(r'^historico_alteracoes/$', views_ciclo.historico_alteracoes, name="historico_alteracoes"),
    
    url(r'^obter_notificacoes_administrador/$', views.obter_notificacoes_do_administrador, name="obter_notificacoes_do_administrador"),
]