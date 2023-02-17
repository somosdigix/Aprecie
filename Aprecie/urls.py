from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from Aprecie import views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Aprecie API')

urlpatterns = [
    path('api/', schema_view),
    path(r'', views.login),
    path(r'app/', views.index),
    path(r'login/', include('Login.urls')),
    path(r'reconhecimentos/', include('Reconhecimentos.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)