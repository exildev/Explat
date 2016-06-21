from django.conf.urls import patterns, url
from django.views.generic import TemplateView
import views

# Gestion de motorizado
urlpatterns = [
    url(r'^motorizado/add/$', views.add_motorizado, name='add_motorizado'),
    url(r'^motorizado/search/$', views.searchMotorizado, name='search_motorizado'),
    url(r'^motorizado/list/$', TemplateView.as_view(
        template_name='motorizado/motorizado.html'), name='list_motorizado'),
    url(r'^motorizado/edit/(?P<motorizado_id>\d+)/$',
        views.editMotorizado, name='edit_motorizado'),
    url(r'^moto/details/(?P<moto_id>\d+)/$',
        views.infoMoto, name='api_info_moto'),
    url(r'^motorizado/search/pedido/$', views.SearchMotorizadoPed.as_view(), name='search_pedido_motorizado'),
]

# Gestion de despacho
urlpatterns += [
    url(r'^rastreo/$', TemplateView.as_view(template_name='motorizado/rastreo.html'), name='rastreo_motorizado'),
]

# Gestion de Moto
urlpatterns += [
    url(r'^moto/$', TemplateView.as_view(template_name='motorizado/index.html'),
        name="index_moto"),
    url(r'^moto/add/$', views.MotoAdd.as_view(), name='add_moto'),
    url(r'^moto/list/$', TemplateView.as_view(template_name='motorizado/motoSearch.html'), name='list_moto'),
    url(r'^moto/search/$', views.ListMoto, name='search_moto'),
    url(r'^moto/delete/(?P<pk>\d+)/$', views.DeleteMoto, name='delete_moto'),
    url(r'^moto/edit/(?P<pk>\d+)/$', views.EditMoto.as_view(), name='edit_moto'),
    url(r'^moto/asignar/$', views.AsignarMoto.as_view(), name='asignar_moto'),

]

# Gestion de Foto += [
urlpatterns += [
    url(r'^motorizado/foto/$', TemplateView.as_view(template_name='motorizado/foto.html'),
        name='foto_pedido_motorizado'),
]
