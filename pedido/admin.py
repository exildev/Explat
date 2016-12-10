# -*- coding: utf-8 -*-
from django.contrib import admin
import models
import forms
# Register your models here.


class InlineMotivoCancelacionAdmin(admin.StackedInline):
    model = models.MotivoCancelacion
    form =  forms.AddMotivoCancelacionFormAdmin
    extra = 2
# end class


class ConfiguracionPedidoAdmin(admin.ModelAdmin):
    inlines = [InlineMotivoCancelacionAdmin]
    list_display = ['empresa']
    search_fields = ['empresa',]
    fieldsets = [
        (None, {'fields':('empresa',)}),
        ('Tirilla', {'fields':['tirillatp1', 'tirillatp2',]}),
        ('Entrega', {'fields':['cerrartp1', 'cerrartp2',]}),
    ]

    def get_queryset(self, request):
        queryset = super(ConfiguracionPedidoAdmin, self).get_queryset(request)
        return queryset.filter(estado=True)
    # end def

    def get_form(self, request, obj=None, *args, **kwargs):
        if obj:
            kwargs['form'] = forms.EditConfPedidoFormAdmin
        else:
            kwargs['form'] = forms.AddConfPedidoFormAdmin
        # end if
        return super(ConfiguracionPedidoAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def
# end class

class MotivoCancelacionAdmin(admin.ModelAdmin):
    form = forms.AddMotivoCancelacionFormAdmin
    list_display = ['get_empresa', 'nombre', 'descripcion',]
    list_display_links = ['get_empresa']

    def get_empresa(self, obj):
        return obj.configuracion.empresa.first_name if obj.configuracion.empresa else u'------ ----'
    # end class

    get_empresa.allow_tags = True
    get_empresa.short_description = 'Empresa'
# end class
admin.site.register(models.Items)
admin.site.register(models.Pedido)
admin.site.register(models.ConfirmarPedido)
admin.site.register(models.ConfirmarPedidoWs)
admin.site.register(models.CancelarPedido)
admin.site.register(models.CancelarPedidoWs)
admin.site.register(models.ItemsPedido)
admin.site.register(models.PedidoWS)
admin.site.register(models.ConfiguracionTiempo)
admin.site.register(models.ConfiguracionPedido, ConfiguracionPedidoAdmin)
admin.site.register(models.MotivoCancelacion, MotivoCancelacionAdmin)
