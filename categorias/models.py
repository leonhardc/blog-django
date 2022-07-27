from django.db import models


class Categoria(models.Model):
    nome_cat = models.CharField(max_length=50, verbose_name='Categoria') # nome da categoria

    def __str__(self):
        return self.nome_cat
