from django.conf.urls import patterns, url
import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'login/$', views.custom_login, {'template_name': 'usuario/login.html'}, name='user-login'),
    url(r'logout/$', views.custom_logout, {'next_page': '/', }, name='user-logout'),
]


urlpatterns += [
    url(r'session/$', views.Login.as_view(), name='user-login2'),
    url(r'empleado/$', TemplateView.as_view(template_name='usuario/index.html'), name='index'),
    url(r'empleado/add/$', views.EmpleadoAdd.as_view(), name='add_empleado'),
    url(r'empleado/update/states/(?P<empleado_id>\d+)/$', views.UpStaCliente.as_view(), name='upd_state_empleado'),
    url(r'^empleado/list/$', TemplateView.as_view(template_name='usuario/empleadoSearch.html'), name='list_empleado'),
    url(r'^empleado/search/$', views.searchEmpleadoTabla, name='seach_empleado'),
    url(r'^empleado/details/(?P<empleado_id>\d+)/$', views.infoEmpleado, name='details_empleado'),
    url(r'^empleado/edit/(?P<empleado_id>\d+)/$', views.editEmpleado, name='edit_empleado'),
    url(r'^empleado/edit/pass/(?P<pk>\d+)/$', views.PassChangeEmpleado.as_view(template_name='usuario/passChangeEmpleado.html'), name='edit_pass_empleado'),
    url(r'^$', TemplateView.as_view(template_name='usuario/index_general.html'), name='index_general'),
]


# Gestion de Clientes
urlpatterns += [
    url(r'^cliente/$', views.IndexCliente.as_view(), name='index_cliente'),
    url(r'^cliente/add/$', views.ClienteAdd.as_view(), name='add_cliente'),
    url(r'^cliente/list/$', TemplateView.as_view(template_name='usuario/clienteSearch.html'), name='list_cliente'),
    url(r'^cliente/search/$', views.searchCliente, name='search_cliente'),
    url(r'^cliente/details/(?P<pk>\d+)/$', views.DetailCliente.as_view(template_name='usuario/infoCliente.html'), name='details_empleado'),
    url(r'^cliente/edit/(?P<pk>\d+)/$', views.UpdateCliente.as_view(template_name='usuario/editCliente.html'), name='edit_cliente'),
]

# Gestion de Tienda
urlpatterns += [
    url(r'^tienda/$', views.IndexTienda.as_view(), name='index_tienda'),
    url(r'^tienda/add/$', views.AddTienda.as_view(), name='add_tienda'),
    url(r'^tienda/edit/(?P<pk>\d+)/$', views.UpdateTienda.as_view(), name='update_tienda'),
    url(r'^tienda/details/(?P<pk>\d+)/$', views.DetailTienda.as_view(), name='details_tienda'),
    url(r'^tienda/delete/(?P<pk>\d+)/$', views.DeleteTienda.as_view(), name='delete_tienda'),
    url(r'^tienda/list/$', views.ListTienda.as_view(), name='list_tienda'),
    url(r'^tienda/list/search/$', views.TablaTienda.as_view(), name='search_tienda'),
]


# Gestion servicios de autenticacion
urlpatterns += [
    url(r'tiendas/ws/', views.Store.as_view(),name='get_tiendas'),
]


# Gestion servicios de autenticacion
urlpatterns += [
    url(r'session/', views.Login.as_view(),name='ws_loguin'),
    url(r'logged/', views.is_logged, name="is_logged"),
]
