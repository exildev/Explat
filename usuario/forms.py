# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets
import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tu usuario', 'autofocus': True}), max_length=254)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña'}))
# end class


class AddEmpleadoApiForm(forms.ModelForm):

    class Meta:
        model = models.Empleado
        fields = ('username', 'first_name', 'last_name', 'tipo_id', 'identificacion', 'cargo', 'fecha_nacimiento',
                  'empresa', 'password', 'telefono_fijo', 'telefono_celular', 'email', 'direccion', 'ciudad')
        exclude = ('empresa',)
        widgets = {
            "username": forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'}),
            "first_name": forms.TextInput(attrs={'placeholder': 'Nombres', 'required': True}),
            "last_name": forms.TextInput(attrs={'placeholder': 'Apellidos', 'required': True}),
            "identificacion": forms.TextInput(attrs={'placeholder': 'Numero de Identificación'}),
            "telefono_fijo": forms.TextInput(attrs={'placeholder': 'Telefono Fijo'}),
            "telefono_celular": forms.TextInput(attrs={'placeholder': 'Telefono Celular'}),
            "direccion": forms.TextInput(attrs={'placeholder': 'Direccion'}),
            "ciudad": forms.Select(attrs={'class': 'ui search dropdown'}),
            "tipo_id": forms.Select(attrs={'class': 'ui dropdown'}),
            "cargo": forms.Select(attrs={'class': 'ui dropdown'}),
            "fecha_nacimiento": forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder': 'Ingrese Fecha de Nacimiento 31/12/2015', 'type': 'date'}),
            "password": forms.PasswordInput(attrs={'placeholder': 'Ingrese Contraseña'}),
            "email": forms.EmailInput(attrs={'Placeholder': 'Email', 'required': True}),
        }

    def save(self, commit=True):
        self.instance.password = make_password(self.instance.password)
        return super(AddEmpleadoApiForm, self).save(commit)
    # end def
# end class


class AddEmpleadoApiForm(forms.ModelForm):

    class Meta:
        model = models.Empleado
        fields = ('username', 'first_name', 'last_name', 'tipo_id', 'identificacion', 'cargo', 'fecha_nacimiento',
                  'empresa', 'password', 'telefono_fijo', 'telefono_celular', 'email', 'direccion', 'ciudad')
        exclude = ('empresa',)
        widgets = {
            "username": forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'}),
            "first_name": forms.TextInput(attrs={'placeholder': 'Nombres', 'required': True}),
            "last_name": forms.TextInput(attrs={'placeholder': 'Apellidos', 'required': True}),
            "identificacion": forms.TextInput(attrs={'placeholder': 'Numero de Identificación'}),
            "telefono_fijo": forms.TextInput(attrs={'placeholder': 'Telefono Fijo'}),
            "telefono_celular": forms.TextInput(attrs={'placeholder': 'Telefono Celular'}),
            "direccion": forms.TextInput(attrs={'placeholder': 'Direccion'}),
            "ciudad": forms.Select(attrs={'class': 'ui search dropdown'}),
            "tipo_id": forms.Select(attrs={'class': 'ui dropdown'}),
            "cargo": forms.Select(attrs={'class': 'ui dropdown'}),
            "fecha_nacimiento": forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder': 'Ingrese Fecha de Nacimiento 31/12/2015', 'type': 'date'}),
            "password": forms.PasswordInput(attrs={'placeholder': 'Ingrese Contraseña'}),
            "email": forms.EmailInput(attrs={'Placeholder': 'Email', 'required': True}),
        }

    def save(self, commit=True):
        self.instance.password = make_password(self.instance.password)
        return super(AddEmpleadoApiForm, self).save(commit)
    # end def
# end class


class EditEmpleadoApiForm(forms.ModelForm):

    class Meta:
        model = models.Empleado
        fields = ('username', 'first_name', 'last_name', 'tipo_id', 'identificacion', 'cargo',
                  'fecha_nacimiento', 'empresa', 'telefono_fijo', 'telefono_celular', 'email', 'direccion', 'ciudad')
        exclude = ('empresa',)
        widgets = {
            "username": forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'}),
            "first_name": forms.TextInput(attrs={'placeholder': 'Nombres', 'required': True}),
            "last_name": forms.TextInput(attrs={'placeholder': 'Apellidos', 'required': True}),
            "identificacion": forms.TextInput(attrs={'placeholder': 'Numero de Identificación'}),
            "telefono_fijo": forms.TextInput(attrs={'placeholder': 'Telefono Fijo'}),
            "telefono_celular": forms.TextInput(attrs={'placeholder': 'Telefono Celular'}),
            "direccion": forms.TextInput(attrs={'placeholder': 'Direccion'}),
            "ciudad": forms.Select(attrs={'class': 'ui search dropdown'}),
            "tipo_id": forms.Select(attrs={'class': 'ui dropdown'}),
            "cargo": forms.Select(attrs={'class': 'ui dropdown'}),
            "fecha_nacimiento": forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder': 'Ingrese Fecha de Nacimiento 31/12/2015', 'type': 'date'}),
            "email": forms.EmailInput(attrs={'Placeholder': 'Email', 'required': True}),
        }
# end class


class AddClienteForm(forms.ModelForm):

    class Meta:
        model = models.Cliente
        fields = ('first_name', 'last_name', 'tipo_id', 'identificacion',
                  'telefono_fijo', 'telefono_celular', 'direccion', 'barrio', 'zona', 'ciudad')
        widgets = {
            "first_name": forms.TextInput(attrs={'placeholder': 'Nombres'}),
            "last_name": forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            "identificacion": forms.TextInput(attrs={'placeholder': 'Numero de Identificación'}),
            "telefono_fijo": forms.TextInput(attrs={'placeholder': 'Telefono Fijo'}),
            "telefono_celular": forms.TextInput(attrs={'placeholder': 'Telefono Celular'}),
            "direccion": forms.TextInput(attrs={'placeholder': 'Direccion'}),
            "ciudad": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "zona": forms.TextInput(attrs={'placeholder': 'Zona'}),
            "barrio": forms.TextInput(attrs={'placeholder': 'Barrio'}),
            "tipo_id": forms.Select(attrs={'class': 'ui dropdown'}),
            "empresa": forms.Select(attrs={'class': 'ui dropdown'}),
        }
# end class


class AddEmpleadoForm(forms.ModelForm):

    class Meta:
        model = models.Empleado
        fields = ('username', 'first_name', 'last_name', 'tipo_id', 'identificacion', 'cargo', 'fecha_nacimiento',
                  'empresa', 'password', 'telefono_fijo', 'telefono_celular', 'email', 'direccion', 'ciudad')
        widgets = {
            "username": forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'}),
            "first_name": forms.TextInput(attrs={'placeholder': 'Nombres', 'required': True}),
            "last_name": forms.TextInput(attrs={'placeholder': 'Apellidos', 'required': True}),
            "identificacion": forms.TextInput(attrs={'placeholder': 'Numero de Identificación'}),
            "telefono_fijo": forms.TextInput(attrs={'placeholder': 'Telefono Fijo'}),
            "telefono_celular": forms.TextInput(attrs={'placeholder': 'Telefono Celular'}),
            "direccion": forms.TextInput(attrs={'placeholder': 'Direccion'}),
            "ciudad": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "tipo_id": forms.Select(attrs={'class': 'ui dropdown'}),
            "cargo": forms.Select(attrs={'class': 'ui dropdown'}),
            "fecha_nacimiento": forms.DateInput(attrs={'placeholder': 'Ingrese Fecha de Nacimiento 31/12/2015', 'type': 'date'}),
            "empresa": forms.Select(attrs={'class': 'ui search dropdown'}),
            "password": forms.PasswordInput(attrs={'placeholder': 'Ingrese Contraseña'}),
            "email": forms.EmailInput(attrs={'Placeholder': 'Email', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        print kwargs
        # empresa = kwargs.pop('empresa', 0)
        # self.instance.empresa = models.Empresa.objects.filter(id=1).first()
        super(AddEmpleadoForm, self).__init__(*args, **kwargs)
    # end def

    def save(self, commit=True):
        self.instance.password = make_password(self.instance.password)
        return super(AddEmpleadoForm, self).save(commit)
    # end def
# end class


class PassChangeEmpleadoForm(forms.ModelForm):

    class Meta:
        model = models.Empleado
        fields = ('password',)
        widgets = {
            "password": forms.PasswordInput(attrs={'placeholder': 'Ingrese Nueva Contraseña'}),
        }

    def save(self, commit=True):
        self.instance.password = make_password(self.instance.password)
        return super(PassChangeEmpleadoForm, self).save(commit)
    # end def
# end class


class URLInput(forms.TextInput):
    input_type = 'url'


class AddTienda(forms.ModelForm):
    class Meta:
        model = models.Tienda
        fields = ('nit', 'nombre', 'referencia', 'direccion','ciudad', 'url','fijo', 'celular', 'latitud', 'longitud', )
        exclude = ()
        widgets = {
            'nit': forms.TextInput(attrs={'placeholder': 'Nit'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'referencia': forms.TextInput(attrs={'placeholder': 'Nombre de referencia'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'ciudad': forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            'url': URLInput(attrs={'placeholder': 'Url'}),
            'fijo': forms.TextInput(attrs={'placeholder': 'Telefono Fijo'}),
            'celular': forms.TextInput(attrs={'placeholder': 'Celular'}),
            'latitud': forms.NumberInput(attrs={'placeholder': 'Latitud'}),
            'longitud': forms.NumberInput(attrs={'placeholder': 'Longitud'}),
        }
    # end class

    def save(self, commit=True):
        print self
        return super(AddTienda, self).save(commit)
    # end def
# end class
