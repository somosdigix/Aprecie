from django.conf.urls import include, url
import views

urlpatterns = [
	url(r'^testaLogin/$', views.index),
    url(r'^$', views.login_de_funcionario),
    url(r'^entrar/$', views.entrar, name="entrar"),
    url(r'^sair/$', views.sair),
]