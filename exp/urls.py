"""exp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^usuario/', include('usuario.urls', namespace='usuario')),
    url(r'^motorizado/', include('motorizado.urls', namespace='motorizado')),
    url(r'^pedidos/', include('pedido.urls', namespace='pedido')),
    url(r'^reporte/', include('reporte.urls', namespace='reporte')),
    url(r'^$', login_required(views.Index.as_view()), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
