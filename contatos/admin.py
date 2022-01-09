from django.contrib import admin
from . models import Categoria, Contato
# Register your models here.
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email', 'categoria', 'visivel')
    search_fields = ('nome',)
    #list_filetr = ('nome',)
    list_per_page = 10
    #search_fields = ('id', 'nome', 'sobrenome')
    list_editable = ('telefone', 'sobrenome', 'visivel')
admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)



