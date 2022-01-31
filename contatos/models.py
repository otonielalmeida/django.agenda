from django.db import models
from django.utils import timezone
# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=255, default='', editable=False)
    def __str__(self):
        return self.nome
class Contato(models.Model):
    nome = models.CharField(max_length=255, default='')
    sobrenome = models.CharField(max_length=255, blank=True, default='')
    telefone = models.CharField(max_length=50, blank=True, default='')
    email = models.CharField(max_length=255, default='')
    data_criacao = models.DateTimeField(default=timezone.now, blank=True, )
    descricao = models.TextField(blank=True, default='')
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, default='')
    visivel = models.BooleanField(default=True)
    foto = models.ImageField(blank=True, upload_to='fotos/%Y/%m/%d')
    def __str__(self):
        return self.nome