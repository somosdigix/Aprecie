from django.conf.urls import include, url
from django.shortcuts import render, redirect
from django.conf.urls.static import static
from django.conf import settings
from Aprecie import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^app/', views.index),
    url(r'^login/', include('Login.urls')),
    url(r'^reconhecimentos/', include('Reconhecimentos.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)