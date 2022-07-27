from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from publicacoes.models import Publicacoes # para PostIndex()
from django.db.models import Q, Count, Case, When # para ejetar numero de comentarios em
                                                  # PostIndex >> get_queryset()
from comentarios.forms import FormComentario # para a view PostDetalhes()
from comentarios.models import Comentario # para Post_detalhes()
from django.contrib import messages # para Post_detalhes()

# Create your views here.
class PostIndex(ListView):
    model = Publicacoes
    template_name = 'publicacoes/index.html'
    paginate_by = 6
    context_object_name = 'publicacoes' # obejto iteravel que setá usado em index.html

    def get_queryset(self): # sobrescrever método para mudar a ordem de exibição das
                            # publicoes na página
        qs = super().get_queryset()
        qs = qs.select_related('categoria_post')
        qs = qs.order_by('-id').filter(publicado_post=True)
        # ejetar na consulta o numero de comentarios publicados
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(
                        comentario__publicado_comentario=True,
                        then=1
                    )
                )
            )
        )
        return qs

class PostBusca(PostIndex):
    template_name = 'publicacoes/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()

        # print(self.request.GET.get('termo'))
        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) | # ForeignKey
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo) # ForeignKey
        )
        return qs

class PostCategoria(PostIndex):
    template_name = 'publicacoes/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria', None)
        if not categoria:
            return qs

        qs = qs.filter(
            categoria_post__nome_cat__iexact=categoria
        )
        return qs


class PostDetalhes(UpdateView):
    model = Publicacoes
    form_class = FormComentario
    template_name = 'publicacoes/post_detalhes.html'
    context_object_name = 'publicacao'

    # injetando comentários no template post_detalhes.html
    def get_context_data(self, **kwargs):
        contexto = super(PostDetalhes, self).get_context_data(**kwargs)
        post = self.get_object() # obter publicação/post atual
        comentarios = Comentario.objects.filter(
            publicado_comentario=True,
            post_comentario=post.id
        )
        contexto['comentarios'] = comentarios # injeção dos comentários


        return contexto


    # validando formulario
    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.post_comentario = post

        if self.request.user.is_authenticated: # verificando se o usuario está autenticado
            comentario.usuario_comentario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentário enviado com sucesso.')
        return redirect( # redirecionar a pagina
            'post_detalhes',
            pk = post.id
        )

