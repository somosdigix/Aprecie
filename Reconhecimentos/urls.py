from django.urls import path
from Reconhecimentos import views

urlpatterns = [
    path(r'pilares/', views.todos_os_pilares_e_colaboradores, name="todos_os_pilares_e_colaboradores"),
    path(r'reconhecer/', views.reconhecer, name="reconhecer"),
    path(r'ultimos/', views.ultimos_reconhecimentos, name="ultimos_reconhecimentos"),
    path(r'colaborador/<int:id_do_reconhecido>', views.reconhecimentos_do_colaborador, name="reconhecimentos_do_colaborador"),
    path(r'por_reconhecedor/<int:id_do_reconhecido>', views.reconhecimentos_por_reconhecedor, name="reconhecimentos_por_reconhecedor"),
    path(r'todos/<int:id_do_reconhecido>', views.todas_as_apreciacoes, name="todas_as_apreciacoes"),
    path(r'definir_ciclo/', views.definir_ciclo, name="definir_ciclo"),
    path(r'alterar_ciclo/', views.alterar_ciclo, name="alterar_ciclo"),
    path(r'obter_informacoes_ciclo_atual/', views.obter_informacoes_ciclo_atual, name="obter_informacoes_ciclo_atual"),
    path(r'obter_informacoes_ciclo_futuro/', views.obter_informacoes_ciclo_futuro, name="obter_informacoes_ciclo_futuro"),
    path(r'ranking/', views.contar_reconhecimentos, name="contar_reconhecimentos"),
    path(r'<int:id_do_reconhecido>/<int:id_do_pilar>', views.reconhecimentos_por_pilar, name="reconhecimentos_por_pilar"),
    path(r'ciclos_passados/', views.ciclos_passados, name="ciclos_passados"),
    path(r'historico_alteracoes/', views.historico_alteracoes, name="historico_alteracoes"),
    path(r'ranking_por_periodo/', views.ranking_por_periodo, name="ranking_por_periodo"),
    path(r'obter_notificacoes_administrador/', views.obter_notificacoes_do_administrador, name="obter_notificacoes_do_administrador"),
]
