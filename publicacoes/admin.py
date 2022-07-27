from django.contrib import admin
from .models import Publicacoes
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
class PublicacoesAdmin(SummernoteModelAdmin):
    list_display = (
        'id',
        'titulo_post',
        'autor_post',
        'data_post',
        'categoria_post',
        'publicado_post',
    )
    list_editable = (
        'publicado_post',
    )
    list_display_links = (
        'id',
        'titulo_post',
    )
    summernote_fields = (
        'conteudo_post',
    )

admin.site.register(Publicacoes, PublicacoesAdmin)