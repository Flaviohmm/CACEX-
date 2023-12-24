from django.contrib import admin
from .models import Nome, Setor, Municipio, Atividade, RegistroAtividade


admin.site.register(Nome)
admin.site.register(Setor)
admin.site.register(Municipio)
admin.site.register(Atividade)
admin.site.register(RegistroAtividade)
