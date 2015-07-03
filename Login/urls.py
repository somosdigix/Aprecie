from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$', views.login_de_funcionario),
    url(r'^logar/$', views.logar),
]