from django import forms
# from django.contrib.admin.widgets import AdminDateWidget
# from django.forms import widgets
from .models import Formulari, Prezzi, Anagrafica, Ripartizioni, Materiali, Riepiloghi
from django.utils.translation import gettext_lazy as _


class FormulariForm(forms.ModelForm):

    class Meta:
        model = Formulari
        fields = ('comm', 'cod', 'mat', 'data', 'prod',
                  'qu', 'um', 'prez', 'ripa', 'stato')
        widgets = {
            'data': forms.DateInput(attrs={'id': 'datepicker'}),
            'cod': forms.TextInput(attrs={'id': 'target'})
        }
        labels = {
            'comm': _('Commerciante'),
            'cod': _('Codice'),
            'prod': _('Produttore'),
            'qu': _('Quantita'),
            'um': _('Unita di Misura'),
            'ripa': _('Ripartizione'),
            'prez': _('Prezzo'),
            'mat': _('Materiali'),
        }


class AnagraficaForm(forms.ModelForm):

    class Meta:
        model = Anagrafica
        fields = ('nome', 'mail', 'riferimento', 'tel', 'addr', 'note')
        widgets = {
            'mail': forms.EmailInput,
        }


class RipartizioniForm(forms.ModelForm):

    class Meta:
        model = Ripartizioni
        fields = ('nome', 'mail', 'riferimento', 'tel', 'note')


class PrezziForm(forms.ModelForm):

    class Meta:
        model = Prezzi
        fields = ('comm', 'mat', 'um', 'valore', 'data', 'note')
        widgets = {
            'data': forms.DateInput(attrs={'id': 'datepicker'}),
        }
        labels = {
            'comm': _('Commerciante'),
            'mat': _('Materiale'),
            'um': _('Unita di Misura'),
        }


class MaterialiForm(forms.ModelForm):

    class Meta:
        model = Materiali
        fields = ('mat', 'cod')
        labels = {
            'cod': _('Codice CER'),
            'mat': _('Materiale'),
        }


class RiepiloghiForm(forms.ModelForm):

    class Meta:
        model = Riepiloghi
        fields = ('comm', 'data', 'autore', 'doc', 'ric', 'stato')
        widgets = {
            'data': forms.DateInput(attrs={'id': 'datepicker'}),
        }
        labels = {
            'comm': _('Commerciante'),
            'doc': _('Documento'),
            'ric': _('Ricevuta'),
        }
