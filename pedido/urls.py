from django.conf.urls import patterns, url
import views
from django.views.generic import TemplateView

# Gestion de pedido
urlpatterns = [
    url(r'^pedido/$', TemplateView.as_view(template_name='pedido/index.html'), name='index_pedido'),
    url(r'^pedido/admin/add/$', views.AddPedidoAdmin.as_view(), name='add_admin_pedido'),
    url(r'^pedido/edit/(?P<pk>\d+)/$', views.EditPedido.as_view(), name='edit_pedido'),
    url(r'^pedido/info/(?P<pk>\d+)/$', views.InfoPedido.as_view(), name='info_pedido'),
    url(r'^pedido/factura/(?P<pk>\d+)/$', views.FacturaPedido.as_view(template_name='pedido/factura.html'), name='factura_pedido'),
    url(r'^pedido/list/$', TemplateView.as_view(template_name='pedido/pedidosSearch.html'), name='list_pedido'),
    url(r'^pedido/search/$', views.TablaPedido.as_view(), name='search_pedido'),
    url(r'^pedido/mis/$', views.MisPedidos.as_view(), name='mis_pedido'),
    url(r'^pedido/mis/pedidos/$', views.TablaMisPedidos.as_view(), name='pedidos_pedido'),
]

# Gestion de despacho
urlpatterns += [
    url(r'^despacho/$', views.Despacho.as_view(), name='despachar_pedido'),
    url(r'^pedido/despacho/search/$', views.TablaDespachoPedido.as_view(), name='despachar_search_pedido'),
    url(r'^pedido/despacho/update/$', views.UpdateServicePedido.as_view(), name='despachar_update_pedido'),
    url(r'^pedido/entrega/update/$', views.UpdateEntregaServicePedido.as_view(), name='entrega_update_pedido'),
]

# Gestion de Item
urlpatterns += [
    url(r'^pedido/add/item/(?P<pk>\d+)/$', views.AddItemPedido.as_view(), name='add_item_pedido'),
    url(r'^pedido/finalizar/(?P<pk>\d+)/$', views.FinalizarPedido.as_view(), name='final_item_pedido'),
    url(r'^item/add/$', views.AddItem.as_view(), name='add_item'),
    url(r'^item/edit/(?P<pk>\d+)/$', views.UpdateItem.as_view(), name='edit_item'),
    url(r'^item/list/$', TemplateView.as_view(template_name='pedido/itemsSearch.html'), name='list_item'),
    url(r'^item/search/$', views.TablaItems.as_view(), name='search_item'),
    url(r'^item/delete/(?P<pk>\d+)/(?P<id_pedido>\d+)/$', views.DeleteItemPedido.as_view(), name='delete_item_pedido'),
]

# Gestion Asignacion Motorizado a Pedido
urlpatterns += [
    url(r'^asignar/motorizado/$', TemplateView.as_view(template_name='pedido/asignarMotorizado.html'), name='asignar_motorizado_pedido'),
    url(r'^asignar/motorizado/search/$', views.TablaPedidosAsignar.as_view(), name='tabla_asignar_motorizado_pedido'),
    url(r'^asignar/motorizado/pedido/(?P<pedido_id>\d+)/$', views.AsignarPedidoMotorizado.as_view(), name='motorizado_asignar_pedido'),
    url(r'^asignar/motorizado/close/(?P<pedido_id>\d+)/$', views.CAMotorizado.as_view(), name='motorizado_cerrar_asignar_pedido'),

]

# Getsion de actualizacion de pedidos
urlpatterns += [
    url(r'^motorizado/up/ser/pedido/$', views.UpSerPedido.as_view(), name='mot_up_serPedido'),
    url(r'^motorizado/up/ser/entrega/$', views.UpdPedSerEntrega.as_view(), name='up_ser_entrega_pedido'),
]


# Getsion de actualizacion de pedidos
urlpatterns += [
    url(r'^emp/ws/pedido/$', views.WsPedidoEmpresa.as_view(), name='ws_serPedido'),
]


# Gestion de Ws
urlpatterns += [
    url(r'^rastreo/$', views.Rastreo.as_view(), name='rastreo'),
    url(r'^res/ws/pedido/$', views.UpSerPedido.as_view(), name='up_serPedido'),
]


# Gestion de recepcion de pedido
urlpatterns += [
    url(r'^aceptar/pws/$', views.AceptarPWService.as_view(), name='aceptar_pwservice'),
    url(r'^aceptar/pplataforma/$', views.AceptarPPlataforma.as_view(), name='aceptar_pplataforma'),
]


# Gestion de recoger de pedido
urlpatterns += [
    url(r'^recoger/pplataforma/$', views.RecogerPPlataforma.as_view(), name='recoger_pplataforma'),
    url(r'^recoger/pws/$', views.RecogerPWService.as_view(), name='recoger_wservice'),
]


# Gestion de recoger de pedido
urlpatterns += [
    url(r'^entregar/pplataforma/$', views.EntregarPPlataforma.as_view(), name='entregar_pplataforma'),
    url(r'^entregar/pws/$', views.EntregarPWService.as_view(), name='entregar_wservice'),
]
