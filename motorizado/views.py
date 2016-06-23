from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from exp.decorators import *
from usuario import models as usuario
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import models
import forms
from supra import views as supra
from django.views.generic import View
from usuario import models as usuario
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from usuario import models as usuario
from django.core.exceptions import PermissionDenied
from exp.decorators import administrador_required, supervisor_required


def add_motorizado(request):
    user = models.Empleado.objects.filter(username=request.user).first()
    empresa = usuario.Empresa.objects.filter(first_name=user.empresa).first()
    motosC = models.Moto.objects.filter(empresaM=empresa).filter(
        motorizado__moto__isnull=True).count()
    empleadosC = usuario.Empleado.objects.filter(cargo='MOTORIZADO').filter(
        empresa=empresa, motorizado__empleado__isnull=True).count()
    if motosC > 0:
        return redirect(reverse('motorizado:asignar_moto'))
    else:
        if empleadosC > 0:
            if request.method == 'POST':
                formMoto = forms.AddMotoApiForm(
                    request.POST, instance=models.Moto())
                formSoat = forms.AddSoatForm(
                    request.POST, instance=models.Soat())
                formTecno = forms.AddTecnoForm(
                    request.POST, instance=models.Tecno())
                formMotorizado = forms.AddMotorizadoForm(
                    request.POST, instance=models.Motorizado())
                if formSoat.is_valid() and formTecno.is_valid() and formMoto.is_valid() and formMotorizado.is_valid():
                    new_soat = formSoat.save()
                    new_tecno = formTecno.save()
                    new_moto = formMoto.save(commit=False)
                    new_moto.tecno = new_tecno
                    new_moto.soat = new_soat
                    new_moto.empresaM = empresa
                    new_moto.save()
                    new_motorizado = formMotorizado.save(commit=False)
                    new_motorizado.moto = new_moto
                    new_motorizado.save()
                    mensaje = {
                        'tipo': 'success', 'texto': "Se a registrado un motorizado correctamente"}
                    msg = {'mensaje': mensaje, 'formSoat': formSoat, 'formTecno': formTecno,
                           'formMoto': formMoto, 'formMotorizado': formMotorizado}
                    return render(request, 'motorizado/addMotorizado.html', msg)
            else:
                formMoto = forms.AddMotoApiForm(instance=models.Moto())
                formSoat = forms.AddSoatForm(instance=models.Soat())
                formTecno = forms.AddTecnoForm(instance=models.Tecno())
                formMotorizado = forms.AddMotorizadoApiForm(
                    instance=models.Motorizado())
                formMotorizado.fields["empleado"].queryset = empleadosC = models.Empleado.objects.filter(
                    cargo='MOTORIZADO').filter(empresa=empresa, motorizado__empleado__isnull=True)

            return render(request, 'motorizado/addMotorizado.html', {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto, 'formMotorizado': formMotorizado})
        else:
            return render(request, 'motorizado/addMotorizado.html', {'error': 'No hay empleados disponibles para asignarles una moto'})

@csrf_exempt
def searchMotorizado(request):
    length = request.GET.get('length', '0')
    columnas = ['nombre', 'descripcion']
    num_columno = request.GET.get('order[0][column]', '0')
    order = request.GET.get('order[0][dir]', 0)
    busqueda = request.GET.get('columns[1][search][value]', '')
    start = request.GET.get('start', 0)
    search = request.GET.get('search[value]', False)
    cursor = connection.cursor()
    cursor.execute('select tabla_motorizado(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
        request.user.id, busqueda, order, start, length))
    row = cursor.fetchone()
    return HttpResponse(row[0], content_type="application/json")
# end def


def editMotorizado(request, motorizado_id):
    motorizado = get_object_or_404(models.Motorizado, pk=motorizado_id)
    if request.method == 'POST':
        formMotorizado = forms.editMotorizadoForm(
            request.POST, instance=motorizado)
        if formMotorizado.is_valid():
            formMotorizado.save()
            motorizados = models.Motorizado.objects.filter(
                empleado__id=request.user.id)
            mensaje = {'tipo': 'success',
                       'texto': "Se a editado un motorizado correctamente"}
            return render(request, 'motorizado/motorizado.html', {'mensaje': mensaje, 'motorizados': motorizados})
    else:
        emp = usuario.Empresa.objects.filter(
            empleado__id=request.user.id).values('first_name').first()
        emp = emp['first_name'] if emp else False
        formMotorizado = forms.editMotorizadoForm(instance=motorizado)
    # end if
    return render(request, 'motorizado/editMotorizado.html', {'form': formMotorizado, 'empresa': emp, 'motorizado': motorizado_id})
# end def


def infoMoto(request, moto_id):
    moto = get_object_or_404(models.Moto, pk=moto_id)
    soat = models.Soat.objects.get(numeroS=moto.soat)
    tecno = models.Tecno.objects.get(numeroT=moto.tecno)
    return render(request, 'motorizado/infoMoto.html', {'moto': moto, 'soat': soat, 'tecno': tecno})
# end def


class MotoAdd(View):

    def get(self, request):
        formMoto = forms.AddMotoApiForm(instance=models.Moto())
        formSoat = forms.AddSoatForm(instance=models.Soat())
        formTecno = forms.AddTecnoForm(instance=models.Tecno())
        return render(request, 'motorizado/addMoto.html', {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto})
    # end def

    def post(self, request):
        formMoto = forms.AddMotoApiForm(request.POST, instance=models.Moto())
        formSoat = forms.AddSoatForm(request.POST, instance=models.Soat())
        formTecno = forms.AddTecnoForm(request.POST, instance=models.Tecno())
        if formSoat.is_valid() and formTecno.is_valid() and formMoto.is_valid():
            new_soat = formSoat.save()
            new_tecno = formTecno.save()
            new_moto = formMoto.save(commit=False)
            new_moto.tecno = new_tecno
            new_moto.soat = new_soat
            new_moto.empresaM = usuario.Empresa.objects.filter(
                empleado__id=request.user.id).first()
            new_moto.save()
            mensaje = {'tipo': 'success',
                       'texto': "Se a registrado una moto correctamente"}
            return render(request, 'motorizado/index.html', {'mensaje': mensaje})
        # end if
        return render(request, 'motorizado/addMoto.html', {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto})
# end class


class AsignarMoto(View):

    def get(self, request, *args, **kwargs):
        empleadosC = usuario.Empleado.objects.filter(
            cargo='MOTORIZADO', motorizado__empleado__isnull=True, empresa__empleado__id=request.user.id).first()
        motosC = models.Moto.objects.filter(
            motorizado__moto__isnull=True, estado=True, empresaM__empleado__id=request.user.id).first()
        if empleadosC and motosC:
            form = forms.AsignarMotoForm()
            return render(request, 'motorizado/asignarMoto.html', {'form': form})
        # end if
        error = "No hay motos disponibles  para ser asignadas" if motosC is None else "No hay empleados disponibles para ser asignados"
        return render(request, 'motorizado/asignarMoto.html', {'error': error})
    # end def

    def post(self, request, *args, **kwargs):
        form = forms.AsignarMotoForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = {'tipo': 'success',
                       'texto': "Se a asignado una moto correctamente"}
            return render(request, 'motorizado/index.html', {'mensaje': mensaje})
        # end if
        return render(request, 'motorizado/asignarMoto.html', {'form': form})
    # end def
# end class


@csrf_exempt
def ListMoto(request):
    length = request.GET.get('length', '0')
    columnas = ['nombre', 'descripcion']
    num_columno = request.GET.get('order[0][column]', '0')
    order = request.GET.get('order[0][dir]', 0)
    busqueda = request.GET.get('columns[1][search][value]', '')
    start = request.GET.get('start', 0)
    search = request.GET.get('search[value]', False)
    cursor = connection.cursor()
    cursor.execute('select tabla_moto(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
        request.user.id, busqueda, order, start, length))
    row = cursor.fetchone()
    return HttpResponse(row[0], content_type="application/json")
# end def


class EditMoto(View):

    def get(self, request, *args, **kwargs):
        moto = get_object_or_404(models.Moto, pk=kwargs['pk'])
        soat = models.Soat.objects.filter(numeroS=moto.soat).first()
        tecno = models.Tecno.objects.filter(numeroT=moto.tecno).first()
        formMoto = forms.AddMotoForm(instance=moto)
        formSoat = forms.AddSoatForm(instance=soat)
        formTecno = forms.AddTecnoForm(instance=tecno)
        return render(request, 'motorizado/editMoto.html', {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto, 'pk': kwargs['pk']})
    # end def

    def post(self, request, *args, **kwargs):
        moto = get_object_or_404(models.Moto, pk=kwargs['pk'])
        soat = models.Soat.objects.filter(numeroS=moto.soat).first()
        tecno = models.Tecno.objects.filter(numeroT=moto.tecno).first()
        formMoto = forms.AddMotoApiForm(request.POST, instance=moto)
        formSoat = forms.AddSoatForm(request.POST, instance=soat)
        formTecno = forms.AddTecnoForm(request.POST, instance=tecno)
        empresa = usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa is None:
            raise PermissionDenied
        # end if
        if formSoat.is_valid() and formTecno.is_valid() and formMoto.is_valid():
            new_soat = formSoat.save()
            new_tecno = formTecno.save()
            new_moto = formMoto.save(commit=False)
            new_moto.tecno = new_tecno
            new_moto.soat = new_soat
            new_moto.estado = True
            new_moto.save()
            mensaje = {'tipo': 'positive',
                       'texto': "Se a editado una moto correctamente"}
            return redirect(reverse('motorizado:index_moto'), mensaje)
        # end if
        return render(request, 'motorizado/editMoto.html', {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto, 'pk': kwargs['pk']})
    # end def
# end class


def DeleteMoto(request, pk):
    moto = get_object_or_404(models.Moto, pk=pk).delete()
    return redirect(reverse('motorizado:list_moto'))
# end class


class SearchMotorizadoPed(View):
    def get(self, request):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', '')
        cursor = connection.cursor()
        cursor.execute('select tabla_pedidos_motorizado(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id, search, order, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def


class ListarRastreo(supra.SupraListView):
    model = models.Motorizado
    search_key = 'q'
    list_display = ['nombre', 'apellido', 'identificador', 'placa', 'pk']
    search_fields = ['empleado__first_name', 'empleado__last_name',
                     'licencia', 'identifier', 'moto__placa']
    list_filter = ['empleado__first_name', 'empleado__last_name',
                   'licencia', 'identifier', 'moto__placa']
    paginate_by = 10

    class Renderer:
        nombre = 'empleado__first_name'
        apellido = 'empleado__last_name'
        identificador = 'identifier'
        placa = 'moto__placa'
    # end class
# end class
