from django.conf.urls import include, url
import views

urlpatterns = [
	url(r'^escolher_elogiado/$', views.escolher_elogiado, name="escolher_elogiado"),
    url(r'^reconhecer/$', views.reconhecer, name="reconhecer"),
    url(r'^funcionario/$', views.reconhecimentos_do_funcionario, name="reconhecimentos_do_funcionario"),
]