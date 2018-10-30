from django.shortcuts import render, get_object_or_404, redirect
from .models import Formulari, Anagrafica, Ripartizioni, Prezzi, Materiali, Riepiloghi
from django.utils import timezone
import datetime
from django.template import Context
from django.http import HttpResponse
from django.db.models import Avg, Max, Min, Sum, F, Q, Count, OuterRef, Subquery
from django.db import models
from itertools import chain
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import FormulariForm, AnagraficaForm, PrezziForm, RipartizioniForm, MaterialiForm, RiepiloghiForm
from random import randint
from django.views.generic import TemplateView

#prove grafici
from django.http import JsonResponse
from django.views.generic import View
from formulari.utils import render_to_pdf

#Prove email
from django.core.mail import send_mail, EmailMessage


#Prove
def sendsome(request):
    send_mail(
    'Subject here',
    'Here is the message.',
    'formulari@omg.it',
    ['alberto@fastmail.it'],
    fail_silently=False,
    )
    return redirect('riepiloghi_list')

def send_riepilogo(request,pk,dest):
        eml = EmailMessage(
                'Oggetto',
                'In allegato il riepilogo',
                'alberto@fastmail.it',
                dest)
        eml.attach_file(Riepiloghi.object.get(pk=pk).values('doc'))

# Create your views here.

@login_required(login_url='/login/')
def formulari_list_all(request):
        formulari = Formulari.objects.order_by('-data')
        return render(request, 'formulari/formulari_list.html', {'formularis': formulari})

@login_required(login_url='/login/')
def formulari_list(request):
        formulari = Formulari.objects.filter(~Q(stato='CH'), ~Q(stato='IA')).order_by('-data')
        return render(request, 'formulari/formulari_list.html', {'formularis': formulari})

@login_required(login_url='/login/')
def formulari_new(request):
    if request.method == "POST":
        form = FormulariForm(request.POST)
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.autore = request.user
	    formulario.imp = formulario.prez * formulario.qu
            formulario.save()
            return redirect('formulari_detail', pk=formulario.pk)
    else:
        form = FormulariForm()
    return render(request, 'formulari/formulari_edit.html', {'form': form})


@login_required(login_url='/login/')
def formulari_like(request, rif):
    data_obj = Formulari.objects.filter(pk=rif)
    data = data_obj.values('comm','cod','mat','data','prez','ripa')
    if request.method == "POST":
        form = FormulariForm(request.POST)
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.autore = request.user
            formulario.imp = formulario.prez * formulario.qu
            formulario.save()
            return redirect('formulari_detail', pk=formulario.pk)
    else:
	form = FormulariForm(initial=data[0])
    return render(request, 'formulari/formulari_edit.html', {'form': form})

@login_required(login_url='/login/')
def formulari_detail(request, pk):
	form = get_object_or_404(Formulari, pk=pk)
        return render(request, 'formulari/formulari_details.html', {'form': form})


@login_required(login_url='/login/')
def formulari_edit(request, pk):
    formulario = get_object_or_404(Formulari, pk=pk)
    if request.method == "POST":
        form = FormulariForm(request.POST, instance=formulario)
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.autore = request.user
            formulario.imp = formulario.prez * formulario.qu
            formulario.save()
            return redirect('formulari_detail', pk=formulario.pk)
    else:
        form = FormulariForm(instance=formulario)
    return render(request, 'formulari/formulari_edit.html', {'form': form})

@login_required(login_url='/login/')
def formulari_delete(request, pk):
        form = get_object_or_404(Formulari, pk=pk)
	Formulari.objects.filter(pk=form.pk).delete()
        formulari = Formulari.objects.order_by('data')
        return render(request, 'formulari/formulari_list.html', {'formularis': formulari})

@login_required(login_url='/login/')
def formulari_delete_all(request):
	Formulari.objects.all().delete()
	return redirect('formulari_list')

@login_required(login_url='/login/')
def formulari_change(request,pk,cod):
        fo = get_object_or_404(Formulari, pk=pk)
        fo.stato=cod
        fo.save()
        return redirect('formulari_detail', pk=fo.pk)

@login_required(login_url='/login/')
def formulari_orfani(request):
	formulari = Formulari.objects.filter(riepi=None).order_by('-data')
        return render(request, 'formulari/formulari_list.html', {'formularis': formulari})

# Anagrafica

@login_required(login_url='/login/')
def anagrafica_list(request):
	array = Anagrafica.objects.annotate(doc_ap=Subquery(Anagrafica.objects.filter(pk=OuterRef('pk')).filter(formulari__stato="AP").annotate(doc_ap=Count('formulari')).values('doc_ap'),output_field=models.IntegerField()))
	context = { 'arrays':array }
        return render(request, 'formulari/anagrafica_list.html', context)


@login_required(login_url='/login/')
def anagrafica_new(request):
    if request.method == "POST":
        form = AnagraficaForm(request.POST)
        if form.is_valid():
            anagrafica = form.save(commit=False)
            anagrafica.save()
            return redirect('anagrafica_detail', pk=anagrafica.pk)
    else:
       	form = AnagraficaForm()
    return render(request, 'formulari/anagrafica_edit.html', {'form': form})

@login_required(login_url='/login/')
def anagrafica_edit(request, pk):
    record = get_object_or_404(Anagrafica, pk=pk)
    if request.method == "POST":
        form = AnagraficaForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.save()
            return redirect('anagrafica_detail', pk=record.pk)
    else:
        form = AnagraficaForm(instance=record)
    return render(request, 'formulari/anagrafica_edit.html', {'form': form})

@login_required(login_url='/login/')
def anagrafica_detail(request, pk):
        record = get_object_or_404(Anagrafica, pk=pk)
        return render(request, 'formulari/anagrafica_details.html', {'record': record})

@login_required(login_url='/login/')
def anagrafica_delete(request, pk):
        form = get_object_or_404(Anagrafica, pk=pk)
        Anagrafica.objects.filter(pk=form.pk).delete()
        return redirect('anagrafica_list')

@login_required(login_url='/login/')
def anagrafica_riepilogo(request, pk):
        fqs = Formulari.objects.filter(comm=pk).filter(stato='AP').order_by('-data')
	gks = []
	fps = []
	gsa = []
	for f1 in fqs :
	  fps.append(f1.pk)
          if f1 and f1.ripa not in gks :
	    gks.append(f1.ripa)
	for g1 in gks :
	    gs = Ripartizioni.objects.filter(formulari__pk__in=fps).filter(pk=g1.pk).annotate(totale=Sum('formulari__imp')).values('nome', 'totale', 'pk')
	    appo = dict(gs[0])
	    gsa.append(appo)
	context = {'fqss':fqs }
	context['gsas'] = gsa
	context['comm'] = pk
	return render(request, 'formulari/formulari_ripa.html', context)

@login_required(login_url='/login/')
def anagrafica_rpdf(request, pk):
        fqs = Formulari.objects.filter(comm=pk).filter(stato='AP').order_by('-data')
        gks = []
	fps = []
        gsa = []
        for f1 in fqs :
	  fps.append(f1.pk)
          if f1 and f1.ripa not in gks :
            gks.append(f1.ripa)
        for g1 in gks :
            gs = Ripartizioni.objects.filter(pk=g1.pk).filter(formulari__pk__in=fps).annotate(totale=Sum('formulari__imp')).values('nome', 'totale', 'pk')
            appo = dict(gs[0])
            gsa.append(appo)
        context = {'fqss':fqs }
        context['gsas'] = gsa
        context['comm'] = Anagrafica.objects.get(id=pk)
	context['data'] = datetime.date.today()
        pdf = render_to_pdf('pdf/formulari_rpdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='/login/')
def anagrafica_preview(request, pk):
        fqs = Formulari.objects.filter(comm=pk).filter(stato='AP').order_by('-data')
        gks = []
        fps = []
        gsa = []
        for f1 in fqs :
          fps.append(f1.pk)
          if f1 and f1.ripa not in gks :
            gks.append(f1.ripa)
        for g1 in gks :
            gs = Ripartizioni.objects.filter(pk=g1.pk).filter(formulari__pk__in=fps).annotate(totale=Sum('formulari__imp')).values('nome', 'totale', 'pk')
            appo = dict(gs[0])
            gsa.append(appo)
        context = {'fqss':fqs }
        context['gsas'] = gsa
        context['comm'] = Anagrafica.objects.get(id=pk)
        context['data'] = datetime.date.today()
        pdf = render_to_pdf('pdf/preview_rpdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='/login/')
def anagrafica_docs(request, pk):
        formulari = Formulari.objects.filter(comm=pk).order_by('-data')
        return render(request, 'formulari/formulari_list.html', {'formularis':formulari})

# Ripartizioni

@login_required(login_url='/login/')
def ripartizioni_list(request):
        array = Ripartizioni.objects.order_by('nome')
        return render(request, 'formulari/ripartizioni_list.html', {'arrays': array})

@login_required(login_url='/login/')
def ripartizioni_detail(request, pk):
        record = get_object_or_404(Ripartizioni, pk=pk)
#	if record:
#	  num_doc = Formulari.objects.filter(ripa=pk)
        return render(request, 'formulari/ripartizioni_details.html', {'record': record})

@login_required(login_url='/login/')
def ripartizioni_new(request):
    if request.method == "POST":
        form = RipartizioniForm(request.POST)
        if form.is_valid():
            anagrafica = form.save(commit=False)
            anagrafica.save()
            return redirect('ripartizioni_detail', pk=anagrafica.pk)
    else:
        form = RipartizioniForm()
    return render(request, 'formulari/ripartizioni_edit.html', {'form': form})

@login_required(login_url='/login/')
def ripartizioni_edit(request, pk):
    record = get_object_or_404(Ripartizioni, pk=pk)
    if request.method == "POST":
        form = RipartizioniForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.save()
            return redirect('ripartizioni_detail', pk=record.pk)
    else:
        form = RipartizioniForm(instance=record)
    return render(request, 'formulari/ripartizioni_edit.html', {'form': form})

@login_required(login_url='/login/')
def ripartizioni_delete(request, pk):
        form = get_object_or_404(Ripartizioni, pk=pk)
        Ripartizioni.objects.filter(pk=form.pk).delete()
        return redirect('ripartizioni_list')

@login_required(login_url='/login/')
def ripartizioni_riepilogo(request, pk):
        formulari = Formulari.objects.filter(ripa=pk)
        return render(request, 'formulari/formulari_list.html', {'formularis':formulari})

def ripartizioni_bilancio(request, pk):
        data=dict()        
        for i in Materiali.objects.all():
                incassi = Formulari.objects.filter(ripa__pk=pk).filter(mat__pk=i.pk).aggregate(Sum('imp'))
                if incassi['imp__sum'] is not None :
                        data[str(i)] = incassi['imp__sum']
        result = {
                "labels":data.keys(),
                "default":data.values(),                
        }
        return JsonResponse(result)
# Prezzi

@login_required(login_url='/login/')
def prezzi_list(request):
	array = Prezzi.objects.order_by('-data')
	return render(request, 'formulari/prezzi_list.html', {'arrays': array})


@login_required(login_url='/login/')
def prezzi_chart(request):
    prezzi_data = []
    prezzi_chart = []
    prezzi_data = Prezzi.objects.order_by('-data').values_list('data', flat=True)
    prezzi_chart = Prezzi.objects.order_by('-data').values_list('valore', flat=True)
    context = {'prezzi_data' : list(prezzi_data)}
    context['prezzi_chart'] = list(prezzi_chart)
    return render(request, 'formulari/prezzi_chart.html', context )


@login_required(login_url='/login/')
def prezzi_new(request):
    if request.method == "POST":
        form = PrezziForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
	    record.autore = request.user
            record.save()
            return redirect('prezzi_list')
    else:
        form = PrezziForm()
    return render(request, 'formulari/prezzi_edit.html', {'form': form})

@login_required(login_url='/login/')
def prezzi_ultimi(request):
	values = []
	qs = Anagrafica.objects.all()
	ms = Materiali.objects.all()
	for q1 in qs :
	  for m1 in ms :
	    valk = Prezzi.objects.filter(comm__nome=q1).filter(mat__mat=m1.mat).order_by('-data').values('id')[:1]
	    if len(valk) :
	      appo = dict(valk[0])
	      values.append(appo['id'])
	array = Prezzi.objects.filter(pk__in=values)
	return render (request, 'formulari/prezzi_list.html', {'arrays':array})

# Materiali

@login_required(login_url='/login/')
def materiali_list(request):
	array = Materiali.objects.order_by('cod')
	return render(request, 'formulari/materiali_list.html', {'arrays':array})


@login_required(login_url='/login/')
def materiali_new(request):
    title = "Nuovo Prezzo"
    if request.method == "POST":
       	form = MaterialiForm(request.POST)
	context = {'form' : form}
	context['title'] = title
        if form.is_valid():
            record = form.save(commit=False)
            record.autore = request.user
            record.save()
            return redirect('materiali_list')
    else:
        form = MaterialiForm()
        context = {'form' : form}
        context['title'] = title
    return render(request, 'formulari/materiali_edit.html', context )

def mat_mod(request):
    if request.method == "POST":
        form = MaterialiForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.autore = request.user
            record.save()
            return redirect('materiali_list')
    else:
        form = MaterialiForm()
    return render(request, 'formulari/materiali_create_form.html', {'form': form})
# Riepiloghi


@login_required(login_url='/login/')
def riepiloghi_list(request):
        array = Riepiloghi.objects.annotate(totale=Sum('formulari__imp')).order_by('-data')
	return render(request, 'formulari/riepiloghi_list.html', {'arrays':array})

@login_required(login_url='/login/')
def riepiloghi_f_anagrafica(request,pk):
        array = Riepiloghi.objects.filter(comm__pk=pk).annotate(totale=Sum('formulari__imp')).order_by('-data')
        return render(request, 'formulari/riepiloghi_list.html', {'arrays':array})


@login_required(login_url='/login/')
def riepiloghi_details(request,pk):
	formulari = Formulari.objects.filter(riepi=pk).order_by('-data')
	return render(request, 'formulari/formulari_list.html', {'formularis':formulari})


@login_required(login_url='/login/')
def riepiloghi_delete(request, pk):
        form = get_object_or_404(Riepiloghi, pk=pk)
        Riepiloghi.objects.filter(pk=form.pk).delete()
        return redirect('riepiloghi_list')


@login_required(login_url='/login/')
def riepiloghi_generate(request,pk):
	nr = Riepiloghi(comm= Anagrafica.objects.get(pk=pk) , data= datetime.date.today(), autore = request.user, stato = 'PR')
	nr.save()
        fqs = Formulari.objects.filter(comm=pk).filter(stato='AP')
	fqs.update(riepi=nr.pk, stato='RP')
	for step in fqs:
	  step.save()
	return redirect('riepiloghi_details', pk=nr.pk)


@login_required(login_url='/login/')
def riepiloghi_change(request,pk,cod):
	riep = get_object_or_404(Riepiloghi, pk=pk)
	riep.stato=cod
	riep.save()
	if cod == 'PA':
	 fqs = Formulari.objects.filter(riepi=riep.pk)
         fqs.update(stato='CH')
         for step in fqs:
          step.save()
	return redirect('riepiloghi_list')


@login_required(login_url='/login/')
def riepiloghi_upld(request,pk):
    riepilogo = get_object_or_404(Riepiloghi, pk=pk)
    title = "Modifica Riepilogo"
    if request.method == "POST":
        form = RiepiloghiForm(request.POST, request.FILES, instance=riepilogo)
        context = {'form' : form}
	context['title'] = title
        if form.is_valid():
            record = form.save(commit=False)
            record.autore = request.user
            record.save()
            return redirect('riepiloghi_list')
    else:
        form = RiepiloghiForm(instance=riepilogo)
        context = {'form' : form}
	context['title'] = title
    return render(request, 'formulari/materiali_edit.html', context )

    
def comp_r_to_f(cod):
	if (cod == 'RP')or (cod == 'ER'):
	 res = cod
	elif cod == 'IN':
	 res = 'RP'
	elif cod == 'PA':
	 res = 'CH'
	else:
	 res = 'ER'
	return res
