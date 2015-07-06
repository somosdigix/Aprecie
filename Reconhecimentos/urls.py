from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^reconhecer/$', views.reconhecer, name="reconhecer"),
]