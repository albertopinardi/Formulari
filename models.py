from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db.models import Q
# Create your models here.
# Costanti
default_um=1

class Anagrafica(models.Model):
        nome = models.CharField(max_length=200)
        mail = models.EmailField(max_length=200)
        riferimento = models.CharField(max_length=200)
        tel = models.CharField(max_length=200)
	addr = models.CharField(max_length=200,blank=True, null=True)
        note =  models.TextField(blank=True, null=True)

        def __str__(self):
                return self.nome

class Prezzi(models.Model):
        comm = models.ForeignKey('formulari.Anagrafica')
	mat = models.ForeignKey('formulari.Materiali')
        valore = models.CharField(max_length=200)
        data =  models.DateField(blank=True, null=True)
        note =  models.TextField(blank=True, null=True)
	um = models.ForeignKey('formulari.Um', default=default_um)
	autore = models.ForeignKey('auth.User', default=default_um)

	def __unicode__(self):
		return "%s \u20ac/%s" %(self.valore, self.um)
        
        def alla_ton(self):
                if self.um_id == 1:
                        res = float(self.valore)
                elif self.um_id == 3:
                        res = (float(self.valore)*10)
                elif self.um_id == 2:
                        res = (float(self.valore)*1000)
                else:
                        res = (float(self.valore)*0)
                return res

class Formulari(models.Model):
        APERTO = 'AP'
        RIEPI = 'RP'
        CHIUSO = 'CH'
	ERRORE = 'ER'
	INATTIVO = 'IA'
	NODOCS = 'ND'
        SCELTA_STATO = (
                (APERTO, 'Aperto'),
                (RIEPI, 'Riepilogato'),
                (CHIUSO, 'Chiuso'),
                (ERRORE, 'Errore'),
		(INATTIVO, 'Inattivo'),
		(NODOCS, 'No Documenti'),
        )

	comm = models.ForeignKey('formulari.Anagrafica')
	cod = models.CharField(max_length=200)
	data = models.DateField()
	prod = models.ForeignKey('formulari.Produttori', default=default_um )
	mat = models.ForeignKey('formulari.Materiali', default=default_um)
	prez = models.FloatField()
	qu = models.FloatField()
	imp = models.FloatField(blank=True, null=True)
        um = models.ForeignKey('formulari.Um', default=default_um)
	ripa = models.ForeignKey('formulari.Ripartizioni')
        autore = models.ForeignKey('auth.User', default=default_um)
	stato = models.CharField(max_length=2, choices=SCELTA_STATO, default=APERTO,)
	riepi = models.ForeignKey('formulari.Riepiloghi', models.SET_NULL, blank=True, null=True,)


        def __str__(self):
                return self.cod

	def importo(self):
		return "%s \u20ac" %(self.prez * self.qu)

        def importop(self):
                return (self.prez * self.qu)

	def prezzo(self):
		return "%s \u20ac/%s" %(self.prez, self.um)

	def quantita(self):
		return "%s %s" %(self.qu, self.um)

class Materiali(models.Model):
	mat = models.CharField(max_length=200)
	cod = models.CharField(max_length=200)

        def __str__(self):
                return "%s %s" %(self.mat, self.cod)

class Produttori(models.Model):
        nome = models.CharField(max_length=200)
        mail = models.CharField(max_length=200)
        riferimento = models.CharField(max_length=200)
        tel = models.CharField(max_length=200)
        note =  models.TextField(blank=True, null=True)

        def __str__(self):
                return self.nome

class Ripartizioni(models.Model):
        nome = models.CharField(max_length=200)
        mail = models.EmailField(max_length=200)
        riferimento = models.CharField(max_length=200)
        tel = models.CharField(max_length=200)
        note =  models.TextField(blank=True, null=True)

        def __unicode__(self):
                return self.nome

class Um(models.Model):
	nome = models.CharField(max_length=2)

	def __str__(self):
		return self.nome


class Riepiloghi(models.Model):
	PRONTO = 'PR'
	INVIATO = 'IN'
	PAGATO = 'PA'
	ERRORE = 'ER'
        SCELTA_STATO = (
		(PRONTO, 'Pronto'),
                (INVIATO, 'Inviato'),
                (PAGATO, 'Pagato'),
                (ERRORE, 'Errore'),
        )

        comm = models.ForeignKey('formulari.Anagrafica')
        data = models.DateField()
        autore = models.ForeignKey('auth.User', default=default_um)
	doc = models.FileField(upload_to='upld/riepiloghi/',blank=True, null=True)
        ric = models.FileField(upload_to='upld/ricevute/',blank=True, null=True)
        stato = models.CharField(max_length=2, choices=SCELTA_STATO, default=PRONTO,)

	def __str__(self):
		return "R.%s di %s" %(self.pk, self.comm)
