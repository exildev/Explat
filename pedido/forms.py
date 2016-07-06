# -*- coding: utf-8 -*-
from django import forms
import models
from usuario import models as usuario


class AddPedidoApiForm(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = '__all__'
        exclude = ('motorizado', 'total', 'supervisor',
                   'empresa', 'npedido_express',)
        widgets = {
            "num_pedido": forms.TextInput(attrs={'placeholder': 'Numero de Pedido'}),
            "tienda": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "cliente": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "alistador": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "tipo_pago": forms.Select(attrs={'class': 'ui dropdown'}),
            "observacion": forms.Textarea(attrs={'rows': '4', 'placeholder': 'Observaciones'}),
        }


class AddPedidoAdminApiForm(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = '__all__'
        exclude = ('total', 'empresa', 'npedido_express', 'motorizado',)
        widgets = {
            "num_pedido": forms.TextInput(attrs={'placeholder': 'Numero de Pedido'}),
            "tienda": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "cliente": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "tipo_pago": forms.Select(attrs={'class': 'ui dropdown'}),
            "observacion": forms.Textarea(attrs={'rows': '4', 'placeholder': 'Observaciones'}),
            "alistador": forms.Select(attrs={'class': 'ui fluid search selection dropdown', 'required': 'true'}),
            "supervisor": forms.Select(attrs={'class': 'ui fluid search selection dropdown', 'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        empresa = kwargs.pop('num_pedido', 0)
        pedido = models.Pedido.objects.filter(empresa__id=empresa)
        if pedido:
            pedido = pedido.latest('id')
            nom_pedido = '%s_%d' % (pedido.empresa.first_name[0:2].upper(), int(
                pedido.num_pedido.split('_')[1]) + 1)
        elif empresa > 0:
            emp = usuario.Empresa.objects.filter(id=empresa).first()
            nom_pedido = '%s_%d' % (emp.first_name[0:2].upper(), 1)
        else:
            nom_pedido = 'Ex_1'
        # end if
        kwargs.update(initial={
            # 'field': 'value'
            'num_pedido': nom_pedido
        })
        super(AddPedidoAdminApiForm, self).__init__(*args, **kwargs)
        #self.fields['tienda'].queryset = usuario.Tienda.objects.filter(empresa__id=empresa)

class AddItemsApiForm(forms.ModelForm):

    class Meta:
        model = models.Items
        fields = '__all__'
        exclude = ('empresaI',)
        widgets = {
            "codigo": forms.TextInput(attrs={'placeholder': 'Codigo'}),
            "descripcion": forms.Textarea(attrs={'rows': '2', 'placeholder': 'Descripción'}),
            "presentacion": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
        }


class AddItemsForm(forms.ModelForm):

    class Meta:
        model = models.Items
        fields = '__all__'
        widgets = {
            "codigo": forms.TextInput(attrs={'placeholder': 'Codigo'}),
            "descripcion": forms.Textarea(attrs={'rows': '2', 'placeholder': 'Descripción'}),
            "presentacion": forms.Select(attrs={'class': 'ui fluid search selection dropdown', 'placeholder': 'Presentacion'}),
            "empresaI": forms.Select(attrs={'class': 'ui fluid search selection dropdown', 'placeholder': 'Empresa'}),
        }


class AddItemsPedidoForm(forms.ModelForm):

    class Meta:
        model = models.ItemsPedido
        fields = '__all__'
        exclude = ('pedido', 'valor_total',)
        widgets = {
            "cantidad": forms.NumberInput(attrs={'placeholder': 'Cantidad', 'step': '1'}),
            "valor_unitario": forms.NumberInput(attrs={'placeholder': 'Valor Unitario'}),
            "item": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
        }


class EditPedidoAdminApiForm(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = '__all__'
        exclude = ('total', 'empresa', 'npedido_express',)
        widgets = {
            "num_pedido": forms.TextInput(attrs={'placeholder': 'Numero de Pedido'}),
            "tienda": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "cliente": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "tipo_pago": forms.Select(attrs={'class': 'ui dropdown'}),
            "observacion": forms.Textarea(attrs={'rows': '4', 'placeholder': 'Observaciones'}),
            "alistador": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "supervisor": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "motorizado": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(EditPedidoAdminApiForm, self).__init__(*args, **kwargs)
        #self.fields['tienda'].queryset = usuario.Tienda.objects.filter(empresa__id=empresa)


class Cofiguracion(forms.ModelForm):
    class Meta:
        model = models.ConfiguracionTiempo
        fields = ('retraso', 'pedido', 'distancia', 'gps', 'primero', 'segundo',)
        exclude = ('empresa',)
        widgets = {
            'retraso': forms.NumberInput(attrs={'placeholder': 'Tiempo retraso del motorizado'}),
            'pedido': forms.NumberInput(attrs={'placeholder': 'Tiempo de retraso del pedido'}),
            'distancia': forms.NumberInput(attrs={'placeholder': 'Distancia para asignacion de pedido'}),
            'gps': forms.TextInput(attrs={'placeholder': 'Tiempo de envío de Gps'}),
            'primero': forms.NumberInput(attrs={'class': 'Primer corte de quincena'}),
            'segungo': forms.NumberInput(attrs={'placeholder': 'Segungo corte de quincena'}),
        }
    # end class

# end class
