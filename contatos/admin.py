from django.contrib import admin
from . models import Categoria, Contato

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'telefone', 'categoria', 'mostrar')
    list_filter = ('categoria',)
    list_per_page = 10
    search_fields = ('nome', 'sobrenome', 'categoria')
    list_editable = ('telefone', 'mostrar')


admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)
