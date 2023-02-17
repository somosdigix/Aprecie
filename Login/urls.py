from django.urls import path
from Login import views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Aprecie API')

urlpatterns = [
  path(r'api/', schema_view),
  path(r'entrar/', views.entrar, name="entrar"),
  path(r'alterar_foto/', views.alterar_foto, name="alterar_foto"),
  path(r'foto/<int:id_do_colaborador>', views.foto_do_perfil),
  path(r'obter_colaborador/<int:id_colaborador>', views.buscar_colaborador),
  path(r'obter_colaboradores/', views.obter_colaboradores, name="obter_colaboradores"),
  path(r'listagemColaboradoresRh/<str:tipo_ordenacao>', views.buscar_colaboradores_para_RH, name="buscar_colaboradores_para_RH"),
  path(r'colaborador/', views.inserir_colaboradores, name="colaborador"),
  path(r'verificar_usuario/', views.validar_usuario_logado, name="validar_usuario_logado"),
  path(r'administrador/', views.switch_administrador, name="switch_administrador"),
  path(r'obter_administradores/', views.obter_administradores, name="obter_administradores"),
  path(r'obter_logs_administradores/', views.obter_logs_administradores, name="obter_logs_administradores"),
  path(r'usario_discord/<str:usuario_id_do_chat>', views.validar_usuario_id_do_chat, name="validar_usuario_id_do_chat"),
  path(r'colaborador/<int:id_colaborador>', views.editar_colaboradores, name="editar_colaboradores"),
]