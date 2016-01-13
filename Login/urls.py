from django.conf.urls import include, url
from Login import views

urlpatterns = [
    url(r'^entrar/$', views.entrar, name="entrar"),
    url(r'^alterar_foto/$', views.alterar_foto, name="alterar_foto"),
    url(r'^foto/([0-9]+)$', views.foto_do_perfil),
	url(r'^obter_funcionarios/$', views.obter_funcionarios, name="obter_funcionarios"),
]