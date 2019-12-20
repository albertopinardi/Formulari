from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.formulari_list, name='formulari_list'),
    url(r'^all/$', views.formulari_list_all, name='formulari_list_all'),
    url(r'^doc/$', views.formulari_list, name='formulari_list'),
    url(r'^doc/new/$', views.formulari_new, name='formulari_new'),
    url(r'^doc/like/(?P<rif>[0-9]+)/$', views.formulari_like, name='formulari_like'),
    url(r'^doc/(?P<pk>[0-9]+)/$', views.formulari_detail, name='formulari_detail'),
    url(r'^doc/(?P<pk>[0-9]+)/edit/$', views.formulari_edit, name='formulari_edit'),
    url(r'^doc/(?P<pk>[0-9]+)/delete/$', views.formulari_delete, name='formulari_delete'),
    url(r'^doc/(?P<pk>[0-9]+)/change/(?P<cod>[-\w]+)/$', views.formulari_change, name='formulari_change'),
    url(r'^doc/search/$', views.search_formulari, name='search_formulari'),
    url(r'^doc/orfani/$', views.formulari_orfani, name='formulari_orfani'),
    # url(r'^doc/000123/$', views.formulari_delete_all, name='formulari_delete_all'),
    url(r'^commercianti/$', views.anagrafica_list, name='anagrafica_list'),
    url(r'^commercianti/new/$', views.anagrafica_new, name='anagrafica_new'),
    url(r'^commercianti/(?P<pk>[0-9]+)/$', views.anagrafica_detail, name='anagrafica_detail'),
    url(r'^commercianti/(?P<pk>[0-9]+)/edit/$', views.anagrafica_edit, name='anagrafica_edit'),
    url(r'^commercianti/(?P<pk>[0-9]+)/delete/$', views.anagrafica_delete, name='anagrafica_delete'),
    url(r'^commercianti/(?P<pk>[0-9]+)/doc/$', views.anagrafica_docs, name='anagrafica_docs'),
    url(r'^commercianti/(?P<pk>[0-9]+)/riepilogo/$', views.anagrafica_riepilogo, name='anagrafica_riepilogo'),
    url(r'^commercianti/(?P<pk>[0-9]+)/rpdf/$', views.anagrafica_rpdf, name='anagrafica_rpdf'),
    url(r'^commercianti/(?P<pk>[0-9]+)/preview/$', views.anagrafica_preview, name='anagrafica_preview'),
    url(r'^commercianti/(?P<pk>[0-9]+)/riepilogo/new/$', views.riepiloghi_generate, name='riepiloghi_generate'),
    url(r'^gruppi/$', views.ripartizioni_list, name='ripartizioni_list'),
    url(r'^gruppi/new/$', views.ripartizioni_new, name='ripartizioni_new'),
    url(r'^gruppi/(?P<pk>[0-9]+)/$', views.ripartizioni_detail, name='ripartizioni_detail'),
    url(r'^gruppi/(?P<pk>[0-9]+)/edit/$', views.ripartizioni_edit, name='ripartizioni_edit'),
    url(r'^gruppi/(?P<pk>[0-9]+)/doc/$', views.ripartizioni_riepilogo, name='ripartizioni_riepilogo'),
    url(r'^gruppi/(?P<pk>[0-9]+)/delete/$', views.ripartizioni_delete, name='ripartizioni_delete'),
    url(r'^prezzi/$', views.prezzi_list, name='prezzi_list'),
    # url(r'^prezzi/chart/$', views.prezzi_chart, name='prezzi_chart'),
    url(r'^prezzi/new/$', views.prezzi_new, name='prezzi_new'),
    url(r'^prezzi/ultimi/$', views.prezzi_ultimi, name='prezzi_ultimi'),
    url(r'^materiali/$', views.materiali_list, name='materiali_list'),
    url(r'^materiali/new/$', views.materiali_new, name='materiali_new'),
    url(r'^materiali/mod/$', views.mat_mod, name='mat_mod'),
    url(r'^materiali/(?P<pk>[0-9]+)/doc_list/$', views.materiali_group_by, name='materiali_group_by'),
    url(r'^riepiloghi/$', views.riepiloghi_list, name='riepiloghi_list'),
    url(r'^riepiloghi/commercianti/(?P<pk>[0-9]+)/$', views.riepiloghi_f_anagrafica, name='riepiloghi_f_anagrafica'),
    url(r'^riepiloghi/(?P<pk>[0-9]+)/$', views.riepiloghi_details, name='riepiloghi_details'),
    url(r'^riepiloghi/(?P<pk>[0-9]+)/delete/$', views.riepiloghi_delete, name='riepiloghi_delete'),
    url(r'^riepiloghi/(?P<pk>[0-9]+)/change/(?P<cod>[-\w]+)/$', views.riepiloghi_change, name='riepiloghi_change'),
    url(r'^riepiloghi/(?P<pk>[0-9]+)/upld/$', views.riepiloghi_upld, name='riepiloghi_upld'),
    url(r'^riepiloghi/(?P<pk>[0-9]+)/preview/$', views.riepiloghi_preview, name='riepiloghi_preview'),
    # api
    url(r'^api/gruppi/(?P<pk>[0-9]+)/bilancio/$', views.ripartizioni_bilancio, name='ripartizioni_bilancio'),
    url(r'^api/doc_duplicati/$', views.duplicati, name='doc_duplicati'),
    url(r'^api/search_cod/$', views.search_cod, name='search_cod'),
    # prove
    url(r'^sendmail/$', views.sendsome, name='sendmail'),
    url(r'^riepiloghi/(?P<pk>[0-9]+)/mail/$', views.send_riepilogo, name='send_riepilogo'),
    url(r'^materiali/call/$', TemplateView.as_view(template_name='formulari/modal.html'), name='call')

]
