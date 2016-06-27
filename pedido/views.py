# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
import re
from django.views.generic import View, DeleteView
from django.views import generic
from . import forms
from . import models
from motorizado import models as mod_motorizado
from usuario import forms as form_usuario
from usuario import models as mod_usuario
from django.views.generic.edit import FormView, CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.views.generic.edit import UpdateView
from django.db.models import Q, Sum
from easy_pdf.views import PDFTemplateView
from django.template.loader import get_template
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from exp.decorators import administrador_required, alistador_required, supervisor_required
from django.utils.decorators import method_decorator
import json
from socketIO_client import SocketIO, LoggingNamespace


class Despacho(TemplateView):
    template_name = 'pedido/despacharpedido.html'

    @method_decorator(administrador_required)
    @method_decorator(supervisor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Despacho, self).dispatch(request, *args, **kwargs)
    # end def
# end class


class AddPedido(View):

    def get(self, request, *args, **kwargs):
        formP = forms.AddPedidoApiForm()
        formP.fields["alistador"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="ALISTADOR").filter(empresa__empleado__id=request.user.id)
        return render(request, 'pedido/addPedido.html', {'formP': formP})
    # end def
# end class


class AddPedidoAdmin(View):

    def get(self, request, *args, **kwargs):
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa is None:
            return redirect(reverse('pedidos:index_pedido'))
        # end if
        formC = form_usuario.AddClienteForm()
        formP = forms.AddPedidoAdminApiForm(num_pedido=empresa.id)
        formP.fields["alistador"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="ALISTADOR").filter(empresa=empresa)
        formP.fields['tienda'].queryset = mod_usuario.Tienda.objects.filter(
            empresa=empresa)
        formP.fields["supervisor"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="SUPERVISOR").filter(empresa=empresa)
        motori = mod_motorizado.Motorizado.objects.filter(
            empleado__empresa=empresa)
        return render(request, 'pedido/addPedidoAdmin.html',
                      {'formC': formC, 'formP': formP, 'motorizados':
                       mod_motorizado.Motorizado.objects.filter(empleado__empresa=empresa), 'motorizadosE': mod_motorizado.Motorizado.objects.filter(empleado__empresa__username="express")})
    # end def

    def post(self, request, *args, **kwargs):
        print 'Llego 1'
        motorizado = mod_usuario.Empleado.objects.filter(
            identificacion=request.POST['motorizado']).first()
        if motorizado:
            print 'Llego 2'
            formP = forms.AddPedidoAdminApiForm(request.POST)
            empresa = mod_usuario.Empresa.objects.filter(
                empleado__id=request.user.id).first()
            if formP.is_valid():
                print 'Llego 3'
                form = formP.save(commit=False)
                form.motorizado = motorizado
                form.empresa = empresa
                form.save()
                cursor = connection.cursor()
                cursor.execute('select get_add_pedido_admin(%d)' % form.id)
                row = cursor.fetchone()
                return redirect(reverse('pedido:add_item_pedido', kwargs={'pk': form.id}))
            # end if
        # end if
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa is None:
            return redirect(reverse('pedido:index_pedido'))
        # end if
        formC = form_usuario.AddClienteForm()
        formP.fields["alistador"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="ALISTADOR").filter(empresa=empresa)
        formP.fields["supervisor"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="SUPERVISOR").filter(empresa=empresa)
        motori = mod_motorizado.Motorizado.objects.filter(
            empleado__empresa=empresa)
        formP.fields['tienda'].queryset = mod_usuario.Tienda.objects.filter(
            empresa=empresa)
        info = {'formC': formC, 'formP': formP,
                'motorizados': mod_motorizado.Motorizado.objects.filter(empleado__empresa=empresa),
                'motorizadosE': mod_motorizado.Motorizado.objects.filter(empleado__empresa__username="express")}
        return render(request, 'pedido/addPedidoAdmin.html', info)
    # end def
# end class


class EditPedido(FormView):

    def get(self, request, *args, **kwargs):
        pedido = get_object_or_404(models.Pedido, id=kwargs['pk'])
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa:
            pedidoForm = forms.EditPedidoAdminApiForm(instance=pedido)
            pedidoForm.fields["alistador"].queryset = mod_usuario.Empleado.objects.filter(
                cargo="ALISTADOR").filter(empresa=empresa)
            pedidoForm.fields['tienda'].queryset = mod_usuario.Tienda.objects.filter(
                empresa=empresa)
            pedidoForm.fields["supervisor"].queryset = mod_usuario.Empleado.objects.filter(
                cargo="SUPERVISOR").filter(empresa=empresa)
            motorizado = mod_motorizado.Motorizado.objects.filter(
                empleado__empresa=empresa).values_list('id', flat=True)
            pedidoForm.fields["motorizado"].queryset = mod_usuario.Empleado.objects.filter(
                cargo="MOTORIZADO").filter(empresa=empresa, motorizado__id__in=motorizado)
            return render(request, 'pedido/editPedido.html', {'pedidoForm': pedidoForm})
        # end if
        return redirect(reverse('pedido:index_pedido'))
    # end def

    def post(self, request, *args, **kwargs):
        pedido = get_object_or_404(models.Pedido, id=kwargs['pk'])
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        pedidoForm = forms.EditPedidoAdminApiForm(
            request.POST, instance=pedido)
        if pedidoForm.is_valid() and empresa:
            f = pedidoForm.save(commit=False)
            f.empresa = empresa
            f.save()
            return redirect(reverse('pedido:add_item_pedido', kwargs={'pk': f.id}))
        # end if
        pedidoForm.fields['tienda'].queryset = mod_usuario.Tienda.objects.filter(
            empresa=empresa)
        return render(request, 'pedido/editPedido.html', {'pedidoForm': pedidoForm})
    # end def

# end class


class AddItemPedido(View):

    def get(self, request, *args, **kwargs):
        total = 0
        pedido = get_object_or_404(models.Pedido, pk=kwargs['pk'])
        items = models.ItemsPedido.objects.filter(
            pedido=pedido).select_related('item')
        if items:
            resul = items.aggregate(suma=Sum('valor_total'))
            total = resul['suma'] if resul['suma'] is not None else 0
        # end if
        formItems = forms.AddItemsPedidoForm()
        formItems.fields["item"].queryset = models.Items.objects.filter(
            empresaI=pedido.empresa, status=True)
        return render(request, 'pedido/pedidoItems.html', {'pedido': pedido, 'items': items, 'form': formItems, 'total': total})
    # end def

    def post(self, request, *args, **kwargs):
        total = 0
        pedido = get_object_or_404(models.Pedido, pk=kwargs['pk'])
        items = models.ItemsPedido.objects.filter(
            pedido=pedido).select_related('item')
        if items:
            resul = items.aggregate(suma=Sum('valor_total'))
            total = resul['suma'] if resul['suma'] is not None else 0
        formItems = forms.AddItemsPedidoForm(request.POST)
        if formItems.is_valid():
            formI = formItems.save(commit=False)
            formI.pedido = pedido
            formI.valor_total = formI.valor_unitario * formI.cantidad
            formI.save()
            return redirect(reverse('pedido:add_item_pedido', kwargs={'pk': pedido.id}))
        # end if
        return render(request, 'pedido/pedidoItems.html',
                      {'pedido': pedido, 'form': formItems, 'items': items, 'total': total})
        # end if
    # end def
# end class


class FinalizarPedido(View):

    def post(self, request, *args, **kwargs):
        if kwargs['pk']:
            pedido = models.Pedido.objects.filter(id=kwargs['pk']).first()
            if pedido:
                items = models.ItemsPedido.objects.filter(pedido=pedido)
                if items:
                    resul = items.aggregate(suma=Sum('valor_total'))
                    total = resul['suma'] if resul['suma'] is not None else 0
                    if total > 0:
                        models.Pedido.objects.filter(id=kwargs['pk']).update(
                            total=total, confirmado=True)
                        cursor = connection.cursor()
                        cursor.execute(
                            'select get_add_pedido_admin(%d)' % pedido.id)
                        row = cursor.fetchone()
                        lista = json.loads(row[0])
                        if lista:
                            with SocketIO('127.0.0.1', 3000, LoggingNamespace) as socketIO:
                                socketIO.emit('add_pedido_pl', {
                                              'pedido': lista[0], 'tipo': 1})
                                socketIO.wait(seconds=0)
                            # end with
                        # end if
                        return redirect(reverse('pedido:list_pedido'))
                    # end if
                # end if
                error = "No puedes dejar el pedido sin items."
                formItems = forms.AddItemsPedidoForm()
                formItems.fields["item"].queryset = models.Items.objects.filter(
                    empresaI=pedido.empresa, status=True)
                return render(request, 'pedido/pedidoItems.html', {'pedido': pedido, 'items': items, 'form': formItems, 'total': 0, 'error': error})
            # end if
        # end if
        return PermissionDenied
    # end if
# end if


class AddItem(CreateView):
    form_class = forms.AddItemsForm
    model = models.Items
    template_name = 'pedido/addItems.html'

    def post(self, request, *args, **kwargs):
        f = forms.AddItemsApiForm(request.POST)
        if f.is_valid():
            form = f.save(commit=False)
            empresa = models.Empresa.objects.filter(
                empleado__id=request.user.id).first()
            form.empresaI = empresa
            form.status = True
            mensaje = {'tipo': 'success',
                       'texto': 'El item se agregó correctamente'}
            form.save()
            return render(request, 'pedido/addItems.html', {'form': forms.AddItemsApiForm(), 'mensaje': mensaje})
        # end if
        return render(request, 'pedido/addItems.html', {'form': f})
    # end def
# end class


class TablaItems(View):

    @method_decorator(csrf_exempt)
    def get(self, request):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = int(request.GET.get('start', 0))
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        m = 'select tabla_items(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id, busqueda, order, start, length)
        cursor.execute(m)
        row = cursor.fetchone()
        print row
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end def


class UpdateItem(UpdateView):
    model = models.Items
    form_class = forms.AddItemsApiForm
    template_name = 'pedido/editItems.html'

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(models.Items, pk=kwargs['pk'])
        form = forms.AddItemsApiForm(request.POST, instance=item)
        if form.is_valid():
            form.instance.status = True
            form.save()
            mensaje = {'tipo': 'success',
                       'texto': 'El item se actualizó correctamente'}
            return render(request, 'pedido/editItems.html', {'mensaje': mensaje, 'form': form})
        # end if
        return render(request, 'pedido/editItems.html', {'form': form})
# end class


class DeleteItemPedido(DeleteView):
    models = models.ItemsPedido

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(models.ItemsPedido, pk=kwargs['pk'])
        item.delete()
        return redirect(reverse('pedido:add_item_pedido', kwargs={'pk': kwargs['id_pedido']}))
# end class


class TablaPedido(View):

    def get(self, request, *args, **kwargs):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        cursor.execute('select tabla_pedidos(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id, busqueda, order, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class TablaDespachoPedido(View):

    def get(self, request, *args, **kwargs):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        cursor.execute('select tabla_pedidos_despacho(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id, busqueda, order, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class UpdateServicePedido(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # do something
        return super(UpdateServicePedido, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        id_pedido = request.POST['id_ped']
        if id_pedido:
            models.Pedido.objects.filter(
                id=int(id_pedido)).update(despachado=True)
            return HttpResponse("true", content_type="application/json")
        # end if
        return HttpResponse("false", content_type="application/json")
    # end class
# end class


class UpdateEntregaServicePedido(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdateEntregaServicePedido, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        id_pedido = request.POST['id_ped']
        if id_pedido:
            pedido = models.Pedido.objects.filter(id=int(id_pedido)).first()
            if pedido:
                if pedido.despachado:
                    models.Pedido.objects.filter(
                        id=int(id_pedido)).update(entregado=True)
                    return HttpResponse("true", content_type="application/json")
                # end if
            # end if
        # end if
        return HttpResponse("false", content_type="application/json")
    # end def
# end class


class InfoPedido(FormView):

    def get(self, request, *args, **kwargs):
        pedido = get_object_or_404(models.Pedido, pk=kwargs['pk'])
        items = models.ItemsPedido.objects.filter(pedido=pedido)
        return render(request, 'pedido/infoPedido.html', {'pedido': pedido, 'items': items})
    # end def
# end class


class FacturaPedido(PDFTemplateView):
    template_name = "pedido/factura.html"

    def get_context_data(self, **kwargs):
        pedido = get_object_or_404(models.Pedido, pk=kwargs['pk'])
        items = models.ItemsPedido.objects.filter(pedido=pedido)
        empresa = mod_usuario.Empresa.objects.get(first_name=pedido.empresa)
        cliente = mod_usuario.Cliente.objects.get(
            identificacion=pedido.cliente)
        return super(FacturaPedido, self).get_context_data(
            pagesize="A5",
            title="Pedido", pedido=pedido, items=items, empresa=empresa, cliente=cliente,
            **kwargs
        )
    # end def
# end class


class MisPedidos(View):

    def get(self, request):
        empleado = get_object_or_404(mod_usuario.Empleado, pk=request.user.id)
        if empleado:
            if empleado.cargo == 'SUPERVISOR' or empleado.cargo == 'ADMINISTRADOR' or empleado.cargo == 'ALISTADOR':
                return render(request, 'pedido/misPedidos.html')
            else:
                return render(request, 'motorizado/pedidosmotorizado.html')
            # end if
        # end if
        raise PermissionDenied

    # end def
# end class


class TablaMisPedidos(View):

    def get(self, request):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        cursor.execute('select mis_pedidos_asignados(%d,%s,%s)' %
                       (request.user.id, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class TablaPedidosAsignar(View):

    def get(self, request):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        cursor.execute('select pedidos_a_asignar_motor(%d,%s,%s)' %
                       (request.user.id, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class AsignarPedidoMotorizado(View):

    def get(self, request, *args, **kwargs):
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa:
            motorizados = mod_motorizado.Motorizado.objects.filter(
                empleado__empresa=empresa)
            return render(request, 'pedido/chooseMotorizado.html', {'motorizados': motorizados, 'motorizadosE': [], 'pedido': kwargs['pedido_id']})
        # end if
        return PermissionDenied
    # end def
# end class


class CAMotorizado(View):

    def post(self, request, *args, **kwargs):
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if kwargs['pedido_id'] and request.POST['motorizado'] and empresa:
            cursor = connection.cursor()
            cursor.execute('select asignar_motorizado_perr(%s::integer,\'%s\')' % (
                kwargs['pedido_id'], request.POST['motorizado']))
            row = cursor.fetchone()
            if row[0]:
                mensaje = {'tipo': 'success',
                           'texto': 'Se asignó el motorizado correctamente'}
                motorizados = mod_motorizado.Motorizado.objects.filter(
                    empleado__empresa=empresa)
                return render(request, 'pedido/asignarMotorizado.html', {'mensaje': mensaje, 'motorizados': motorizados, 'motorizadosE': [], 'pedido': kwargs['pedido_id']})
            # end if
        # end if
        return PermissionDenied
    # end def
# end class


class UpSerPedido(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpSerPedido, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        id_pedido = request.POST['id_ped']
        if id_pedido:
            models.Pedido.objects.filter(
                id=int(id_pedido)).update(despachado=True)
            return HttpResponse("true", content_type="application/json")
        # end if
        return HttpResponse("false", content_type="application/json")
    # end class
# end class


class UpdPedSerEntrega(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdPedSerEntrega, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        id_pedido = request.POST['id_ped']
        if id_pedido:
            pedido = models.Pedido.objects.filter(id=int(id_pedido)).first()
            if pedido:
                print pedido.despachado, ' Esa es la variable'
                if pedido.despachado:
                    models.Pedido.objects.filter(
                        id=int(id_pedido)).update(entregado=True)
                    return HttpResponse("true", content_type="application/json")
                # end if
            # end if
        # end if
        return HttpResponse("false", content_type="application/json")
    # end def
# end class


class WsPedidoEmpresa(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        print "Esta llegando"
        return super(WsPedidoEmpresa, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('select ws_add_pedido_service(\'%s\'::json)' %
                       request.body.decode('utf-8'))
        row = cursor.fetchone()
        lista = json.loads(row[0])
        if lista['respuesta']:
            if len(lista['pedidos']) > 0:
                with SocketIO('127.0.0.1', 3000, LoggingNamespace) as socketIO:
                    socketIO.emit('add_pedido_ws', {
                                  'pedidos': lista['pedidos'], 'tipo': 2})
                    socketIO.wait(seconds=0)
                # end with
                lista.pop('pedidos')
            # end if
        # end if
        return HttpResponse(json.dumps(lista), content_type="application/json")
    # end def
# end class


class Rastreo(TemplateView):
    template_name = 'pedido/rastreo.html'

    @method_decorator(administrador_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Rastreo, self).dispatch(request, *args, **kwargs)
    # end def
# end class


class RecogerPPlataforma(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RecogerPPlataforma, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        pedido = request.POST.get('pedido', False)
        motorizado = request.POST.get('motorizado', False)
        if pedido and motorizado:
            if re.match('^\d+$', pedido) and re.match('^\d+$', motorizado):
                ped = mod_pedido.PedidoWS.objects.filter(
                    id=int(pedido), morotizado__id=int(mororizado))
                if ped:
                    mod_pedido.PedidoWS.objects.filter(
                        id=int(pedido), morotizado__id=int(mororizado)).update(despachado=True)
                    return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
                # end if
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
# end class


class AceptarPWService(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AceptarPWService, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        print request.POST
        pedido = request.POST.get('pedido', False)
        motorizado = request.POST.get('motorizado', False)
        if pedido and motorizado:
            if re.match('^\d+$', pedido) and re.match('^\d+$', motorizado):
                cursor = connection.cursor()
                cursor.execute('select aceptar_pw_service(%s,\'%s\')' %
                               (pedido, motorizado))
                row = cursor.fetchone()
                res = json.loads(row[0])
                return HttpResponse(row, content_type='application/json', status=200 if res['r'] else 404)
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
    # end class
