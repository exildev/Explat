# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from supra import views as supra
import forms
import models
from django.views.generic.edit import FormView
from exp.decorators import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from motorizado import models as motorizado
# from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import View
from django.views import generic
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import login, logout


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(reverse('usuario:index_general'))
    return login(request, authentication_form=forms.LoginForm, **kwargs)
# end def


def custom_logout(request, **kwargs):
    # Current Django 1.6 uses GET to log out
    if not request.user.is_authenticated():
        return redirect(request.GET.get('next', reverse('usuario:user-login')))
    # end if
    if 'cargo' in request.session and 'empresa' in request.session:
        del request.session["cargo"]
        del request.session["empresa"]
    # end if
    return logout(request, **kwargs)
# end def


class Login(supra.SupraSession):
    pass
# end class


class EmpleadoAdd(View):
    # form_class = forms.AddEmpleadoApiForm

    def get(self, request, *args, **kwargs):
        empresa = models.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        form = forms.AddEmpleadoForm()
        return render(request, 'usuario/addEmpleado.html', {'form': form})
    # end def

    def post(self, request, *args, **kwargs):
        form = forms.AddEmpleadoApiForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.empresa = models.Empresa.objects.filter(
                empleado__id=request.user.id).first()
            form.save()
            if request.POST.get('cargo') and 'MOTORIZADO' in request.POST['cargo']:
                return redirect(reverse('motorizado:add_motorizado'))
            # end if
            mensaje = {'tipo': 'success',
                       'texto': "Se a registrado un empleado correctamente"}
            return render(request, 'usuario/index.html', {'mensaje': mensaje})
        # end if
        return render(request, 'usuario/addEmpleado.html', {'form': form})
    # end def
# end class


@csrf_exempt
def searchEmpleadoTabla(request):
    length = request.GET.get('length', '0')
    columnas = ['nombre', 'descripcion']
    num_columno = request.GET.get('order[0][column]', '0')
    order = request.GET.get('order[0][dir]', 0)
    busqueda = request.GET.get('columns[1][search][value]', '')
    start = request.GET.get('start', 0)
    search = request.GET.get('search[value]', False)
    cursor = connection.cursor()
    cursor.execute('select tabla_empleado(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
        request.user.id, busqueda, order, start, length))
    row = cursor.fetchone()
    return HttpResponse(row[0], content_type="application/json")
# end def


@administrador_required
def infoEmpleado(request, empleado_id):
    empleado = get_object_or_404(models.Empleado, pk=empleado_id)
    motorizado_ = None
    moto = None
    if empleado.cargo == "MOTORIZADO":
        motorizado_ = motorizado.Motorizado.objects.filter(
            empleado=empleado_id).first()
        if motorizado_:
            moto = motorizado_.moto
        # end if
    # end if
    return render(request, 'usuario/infoEmpleado.html', {'empleado': empleado, 'motorizado': motorizado_, 'moto': moto})
# end if


@administrador_required
def editEmpleado(request, empleado_id):
    empleado = get_object_or_404(models.Empleado, pk=empleado_id)
    if request.method == 'POST':
        form = forms.EditEmpleadoApiForm(request.POST, instance=empleado)
        if form.is_valid():
            f = form.save(commit=False)
            f.empresa = models.Empresa.objects.filter(
                empleado__id=request.user.id).first()
            f.save()
            mensaje = {'tipo': 'success',
                       'texto': "Se a editado un empleado correctamente"}
            return render(request, 'usuario/editEmpleado.html', {'mensaje': mensaje, 'form': form, 'empleado': empleado})
    else:
        form = forms.EditEmpleadoApiForm(instance=empleado)
    return render(request, 'usuario/editEmpleado.html', {'form': form, 'empleado': empleado})
# end def


class ClienteAdd(FormView):
    form_class = forms.AddClienteForm
    template_name = 'usuario/addCliente.html'
    model = models.Cliente
    success_url = '/'

    # @method_decorator(administrador_required)
    def post(self, request, *args, **kwargs):
        self.empresa = models.Empresa.objects.filter(
            empleado__pk=request.user.pk).first()
        return super(ClienteAdd, self).post(request, *args, **kwargs)
    # end def

    def form_valid(self, form):
        cliente = form.save(commit=False)
        cliente.empresa = self.empresa
        cliente.save()
        mensaje = {'tipo': 'success',
                   'texto': "Se a registrado un cliente correctamente"}
        return redirect(reverse('usuario:index_cliente'), {'mensaje': mensaje})
    # end def
# end class


@csrf_exempt
def searchCliente(request):
    length = request.GET.get('length', 0)
    columnas = ['nombre', 'descripcion']
    num_columno = request.GET.get('order[0][column]', '0')
    order = request.GET.get('order[0][dir]', 0)
    start = request.GET.get('start', 0)
    search = request.GET.get('search[value]', False)
    busqueda = request.GET.get('columns[1][search][value]', '')
    cursor = connection.cursor()
    cursor.execute('select tabla_cliente(%d,\'%s\'::text,0,%s::integer,%s::integer)' % (
        request.user.id, busqueda, start, length))
    row = cursor.fetchone()
    return HttpResponse(row[0], content_type="application/json")
# end def


class DetailCliente(generic.DetailView):
    model = models.Cliente
    form_class = forms.AddClienteForm
# end class


class UpdateCliente(UpdateView):
    model = models.Cliente
    form_class = forms.AddClienteForm

    def get_success_url(self):
        return reverse('usuario:index_cliente')
    # end def
# end class


class PassChangeEmpleado(UpdateView):
    model = models.Empleado
    form_class = forms.PassChangeEmpleadoForm

    def get(self, request, *args, **kwargs):
        empleado = get_object_or_404(models.Empleado, pk=kwargs['pk'])
        return render(request, 'usuario/passChangeEmpleado.html', {'form': forms.PassChangeEmpleadoForm(), 'empleado': kwargs['pk']})
    # end def

    def post(self, request, *args, **kwargs):
        empleado = get_object_or_404(models.Empleado, pk=kwargs['pk'])
        form = forms.PassChangeEmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            mensaje = {'tipo': 'success', 'texto': "Se a editado la contraseña un empleado correctamente"}
            return render(request, 'usuario/passChangeEmpleado.html', {'form': forms.PassChangeEmpleadoForm(), 'empleado': kwargs['pk'], 'mensaje': mensaje})
        # end def
        return render(request, 'usuario/passChangeEmpleado.html', {'form': form, 'empleado': kwargs['pk'], 'mensaje': mensaje})
    # end def
# end class


class UpStaCliente(View):
    def get(self, request, *args, **kwargs):
        empleado = get_object_or_404(models.Empleado, pk=kwargs['empleado_id'])
        models.Empleado.objects.filter(id=kwargs['empleado_id']).update(is_active=False if empleado.is_active else True)
        return redirect(reverse('usuario:list_empleado'))
    # end def
# end def


class AddTienda(FormView):
    form_class = forms.AddTienda
    template_name = 'usuario/addTienda.html'
    success_url = '/usuario/tienda/add/'

    def post(self, request, *args, **kwargs):
        form = forms.AddTienda(request.POST)
        if form.is_valid():
            addtienda = form.save(commit=False)
            addtienda.empresa = models.Empresa.objects.filter(empleado__id=request.user.id).first()
            addtienda.status = True
            addtienda.save()
            return render(request, 'usuario/addTienda.html', {'mensaje': 'Registro Exitoso', 'form': forms.AddTienda()})
        # end if
        return self.form_invalid(self.get_form(self.get_form_class()))
    # end def
# end class


class UpdateTienda(UpdateView):
    model = models.Tienda
    form_class = forms.AddTienda
    template_name = 'usuario/editTienda.html'

    def get_success_url(self):
        print self.kwargs
        return reverse('usuario:index_cliente')
    # end def
# end class


class DetailTienda(generic.DeleteView):
    template_name = 'usuario/infoTienda.html'
    model = models.Tienda
# end class


class TablaTienda(View):
    def get(self, request):
        length = request.GET.get('length', 0)
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        busqueda = request.GET.get('columns[1][search][value]', '')
        cursor = connection.cursor()
        cursor.execute('select tabla_tienda(%d,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id, busqueda, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class ListTienda(generic.TemplateView):
    template_name = 'usuario/listtienda.html'

    @method_decorator(administrador_required)
    @method_decorator(supervisor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ListTienda, self).dispatch(request, *args, **kwargs)
    # end def
# end class


class IndexTienda(generic.TemplateView):
    template_name = 'usuario/index_tienda.html'

    @method_decorator(administrador_required)
    @method_decorator(supervisor_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexTienda, self).dispatch(request, *args, **kwargs)
    # end def
# end class


class DeleteTienda(View):
    def get(self, request, *args, **kwargs):
        models.Tienda.objects.filter(id=kwargs['pk']).update(status=False)
        return redirect(reverse('usuario:list_tienda'))
    # end def
# end def
