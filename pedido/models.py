from django.db import models
from usuario.models import Cliente,  Empleado,  Empresa, Tienda
import re
from django.core import validators
# Create your models here.


class Items(models.Model):
    PRESENTACION = (
        ('UNIDAD',  'Unidad'),
        ('GRAMO',  'Gramo'),
        ('LITRO',  'Litros')
    )

    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=150)
    presentacion = models.CharField(
        max_length=50,  choices=PRESENTACION,  default='UNIDAD')
    empresaI = models.ForeignKey(Empresa)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.codigo + " - " + self.descripcion


TIPO_PAGO = (
    ('EFECTIVO',  'Efectivo'),
    ('TARJETA',  'Tarjeta'),
    ('REMISION',  'Remision')
)


class Pedido(models.Model):

    num_pedido = models.CharField(max_length=50)
    npedido_express = models.CharField(max_length=50, null=True, blank=True)
    fecha_pedido = models.DateField(auto_now=True)
    tienda = models.CharField(max_length=50,  blank=True,  null=True)
    cliente = models.ForeignKey(Cliente,  null=True)
    supervisor = models.ForeignKey(Empleado,  related_name='supervisor')
    alistador = models.ForeignKey(Empleado,  related_name='alistador')
    motorizado = models.ForeignKey(
        Empleado,  related_name='motorizado_enviado',  null=True)
    tipo_pago = models.CharField(
        max_length=50,  choices=TIPO_PAGO, default='EFECTIVO')
    observacion = models.TextField(max_length=200, null=True, blank=True)
    empresa = models.ForeignKey(Empresa)
    total = models.DecimalField(max_digits=20, decimal_places=2,  null=True)
    entregado = models.BooleanField(default=False)
    despachado = models.BooleanField(default=False)
    confirmado = models.BooleanField(default=False)
    alistado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return self.num_pedido

    def Entregado(self):
        pedido = Pedido.objects.get(npedido_express=self.npedido_express)
        tiempos = Tiempo.objects.get(pedido=pedido)
        return tiempos


class ItemsPedido(models.Model):
    pedido = models.ForeignKey(Pedido)
    item = models.ForeignKey(Items)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, validators=[validators.RegexValidator(re.compile('^[1-9][0-9]*$'), ('numero no valida'), 'invalid')])
    valor_unitario = models.DecimalField(max_digits=20, decimal_places=2, validators=[validators.RegexValidator(re.compile('^[1-9][0-9]*$'), ('numero no valida'), 'invalid')])
    valor_total = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.pedido.num_pedido)
    # end def

    class Meta:
        verbose_name = "Item Pedido"
        verbose_name_plural = "Items Pedido"
    #

class Tiempo(models.Model):
    tiempo_pedido = models.DateTimeField()
    tiempo_asignacion = models.DateTimeField(null=True)
    tiempo_entrego = models.DateTimeField(null=True)
    pedido = models.OneToOneField(Pedido)

    class Meta:
        verbose_name = "Tiempo"
        verbose_name_plural = "Tiempos"


class Time(models.Model):
    creado = models.DateTimeField()
    confirmado = models.DateTimeField(null=True)
    alistado = models.DateTimeField(null=True)
    despachado = models.DateTimeField(null=True)
    entregado = models.DateTimeField(null=True)
    pedido = models.OneToOneField(Pedido)

    class Meta:
        verbose_name = "Time"
        verbose_name_plural = "Times"


class Certificado(models.Model):
    pedidoC = models.ForeignKey(Pedido)
    clienteC = models.ForeignKey(Cliente)
    cedulaC = models.ImageField(upload_to='cedulas/')


class PedidoWS(models.Model):
    num_pedido = models.CharField(max_length=50)
    npedido_express = models.CharField(max_length=50)
    fecha_pedido = models.DateField(auto_now=True)
    cliente = models.CharField(max_length=300,  blank=True,  null=True)
    supervisor = models.ForeignKey(
        Empleado, related_name='supervisorws', null=True)
    alistador = models.ForeignKey(
        Empleado, related_name='alistadorws', null=True)
    motorizado = models.ForeignKey(
        Empleado, related_name='motorizado_enviadows', null=True)
    tipo_pago = models.CharField(max_length=50)
    observacion = models.TextField(max_length=200,  null=True,  blank=True)
    tienda = models.ForeignKey(Tienda, blank=True,  null=True)
    total = models.DecimalField(max_digits=20, decimal_places=2,  null=True)
    entregado = models.BooleanField(default=False)
    despachado = models.BooleanField(default=False)
    confirmado = models.BooleanField(default=False)
    alistado = models.BooleanField(default=False)
    items = models.CharField(max_length=2000,  blank=True,  null=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return self.cliente


class TimeWS(models.Model):
    creado = models.DateTimeField()
    confirmado = models.DateTimeField(null=True)
    alistado = models.DateTimeField(null=True)
    despachado = models.DateTimeField(null=True)
    entregado = models.DateTimeField(null=True)
    pedido = models.OneToOneField(PedidoWS)

    def __str__(self):
        return self.num_pedido
    # end def
# end class



class Punto(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __unicode__(self):
        return '%d - %d' % (self.latitud, self.longitud)
    # end def

# end class


class Seguimiento(models.Model):
    pedido = models.ForeignKey(PedidoWS, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, null=True, blank=True)
    ruta = models.ManyToManyField(Punto)

    def __unicode__(self):
        return '%s' % (self.pedido.num_pedido)
    # end def
# end class
