# -*- coding: UTF-8 -*-
from django.db import models
from lugar.models import Municipio, Departamento
from django.utils.translation import ugettext as _

class Pais(models.Model):
    codigo = models.CharField(_("Codigo"), max_length=2, unique = True, 
                              help_text=_("Codigo pais mas info en: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2"))
    nombre = models.CharField(max_length=100, unique = True)

    def __unicode__(self):
        return "%s(%s)" % (self.nombre, self.codigo)

class TipoDonante(models.Model):
    tipo = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __unicode__(self):
        return self.tipo

class TipoContraparte(models.Model):
    tipo = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __unicode__(self):
        return self.tipo

class Avance(models.Model):
    avance = models.CharField(max_length=100)

    def __unicode__(self):
        return self.avance

class TipoProyecto(models.Model):
    tipo = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.tipo

class Proyecto(models.Model):
    nombre = models.CharField(max_length=400)
    descripcion = models.TextField(_('Descripcion de medidas'))
    avance = models.ForeignKey(Avance)
    tipo = models.ForeignKey(TipoProyecto)
    fecha_inicial = models.DateField() 
    fecha_final = models.DateField() 
    logo = models.ImageField(upload_to='donantes/logos/', blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return "/proyecto/%d/" % self.id

class Donante(models.Model):
    nombre = models.CharField(max_length=150, unique = True)
    descripcion = models.TextField(_('Descripcion del donante'))
    logo = models.ImageField(upload_to='donantes/logos/', blank=True)
    website = models.URLField(blank=True)
    pais = models.ForeignKey(Pais)
    tipo = models.ForeignKey(TipoDonante)

    def __unicode__(self):
        return self.nombre

class Contraparte(models.Model):
    nombre = models.CharField(max_length=150, unique = True)
    pais = models.ForeignKey(Pais)
    tipo = models.ForeignKey(TipoContraparte)
    logo = models.ImageField(upload_to='donantes/logos/', blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.nombre

class ProyectoDepartamento(models.Model):
    '''Modelo usado para agregar todos los municipios y 
    guardar el monto total por departamento'''
    proyecto = models.ForeignKey(Proyecto)
    monto_total = models.FloatField(blank=True, 
                                   help_text=_('rellenar solo si no se dispone' \
                                              'de informacion por municipio'))
    #donantes = models.ManyToManyField(Donante) 
    departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return"%s en %s" % (self.proyecto.nombre, self.departamento.nombre)

class ProyectoMunicipio(models.Model):
    municipio = models.ForeignKey(Municipio)
    monto = models.FloatField()
    donantes = models.ManyToManyField(Donante) 
    contrapartes = models.ManyToManyField(Contraparte) 
    proyecto = models.ForeignKey(ProyectoDepartamento)
    #donante = models.ForeignKey(Donante, blank=True, 
    #                            help_text=_("Puede dejar este campo" \ 
    #                                        "en blanco si no se tiene informacion."))
    #contraparte = models.ForeignKey(Contraparte, blank=True)
    #proyecto = models.ForeignKey(Proyecto)
    
    def __unicode__(self):
        return "%s - %s" % (self.municipio.nombre, self.proyecto.nombre)

class ProyectoDonante(models.Model):
    donante = models.ForeignKey(Donante)
    proyecto = models.ForeignKey(Proyecto)
    monto = models.FloatField(blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.donante.nombre, self.proyecto.nombre)

class ProyectoContraparte(models.Model):
    contraparte = models.ForeignKey(Contraparte)
    proyecto = models.ForeignKey(Proyecto)
    monto = models.FloatField(blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.contraparte.nombre, self.proyecto.nombre)
