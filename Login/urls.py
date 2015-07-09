from django.conf.urls import include, url
import views

urlpatterns = [
	url(r'^obter_funcionarios/$', views.obter_funcionarios, name="obter_funcionarios"),
    url(r'^entrar/$', views.entrar, name="entrar"),
]