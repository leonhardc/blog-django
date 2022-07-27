from django.forms import ModelForm
from .models import Comentario


class FormComentario(ModelForm):

    def clean(self):
        data = self.cleaned_data

        # criando validação
        nome = data.get('nome_comentario')
        email = data.get('email_comentario')
        comentario = data.get('comentario')

        # validação de tamanho de nome
        if len(nome) < 5:
            self.add_error(
                'nome_comentario', # campo a que se refere o erro
                'Nome precisa ter mais de 5 caracteres.' # descrição do erro
            )



    class Meta:
        model = Comentario
        fields = (
            'nome_comentario',
            'email_comentario',
            'comentario',
        )