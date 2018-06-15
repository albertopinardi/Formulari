from django.contrib import admin
from .models import Formulari, Anagrafica, Prezzi, Ripartizioni, Materiali, Produttori, Um, Riepiloghi
# Register your models here.


admin.site.register(Formulari)
admin.site.register(Anagrafica)
admin.site.register(Prezzi)
admin.site.register(Ripartizioni)
admin.site.register(Riepiloghi)
admin.site.register(Materiali)
admin.site.register(Produttori)
admin.site.register(Um)
