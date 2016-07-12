from django.conf.urls import patterns, url
import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# pedidos entregados en la empresa
urlpatterns = [
    url(r'^reporte/$', TemplateView.as_view(template_name='reporte/index.html'), name='index_reporte'),
    url(r'^pedidos/$', TemplateView.as_view(template_name='reporte/pedidos.html'), name='pedidos_reporte'),
    url(r'^pedidos/search/$', views.Pedido.as_view(), name='search_pedidos_reporte'),
]

# pedidos en los que interactua los empleados
urlpatterns += [
    url(r'^empleados/$', views.Empleados.as_view(), name='empleados_reporte'),
    url(r'^load/empleados/$', TemplateView.as_view(template_name='reporte/tablaempleado.html'), name='ajax_empleados_reporte'),
    url(r'^tabla/empleados/$', views.TablaEmpleado.as_view(), name='tabla_empleados_reporte'),
]

# Generacion de informes de empleados
urlpatterns += [
    url(r'^tiempos/empleados/$', views.TiempoEmpleado.as_view(), name='tiempos_empleado_reporte'),
    url(r'^tabla/info/empleados/$', views.TablaInfoEmpleado.as_view(), name='info_tabla_empleados_reporte'),
    url(r'^excel/$', views.Excel.as_view(), name='excel_reporte'),
    url(r'^pdf/$', views.Pdf.as_view(), name='pdf_reporte'),
]
