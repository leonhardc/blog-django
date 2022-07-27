from django.db import models
from categorias.models import Categoria # para o campo categoria_post
from django.contrib.auth.models import User # para o campo de usuário_post
from django.utils import timezone # para o campo data_post


class Publicacoes(models.Model):
    titulo_post = models.CharField(max_length=255, verbose_name='Titulo')
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor')
    data_post = models.DateTimeField(default=timezone.now, verbose_name='Publicado em')
    conteudo_post = models.TextField(verbose_name='Conteudo')
    excerto_post = models.TextField(verbose_name='Excerto')
    categoria_post = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, blank=True,
                                       null=True, verbose_name='Categoria')
    imagem_post = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True,
                                    verbose_name='Imagem')
    publicado_post = models.BooleanField(default=False, verbose_name='Publicar')

    def __str__(self):
        return self.titulo_post