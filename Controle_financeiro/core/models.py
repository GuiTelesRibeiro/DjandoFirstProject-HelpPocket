from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o User do Django
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Entrada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o User do Django
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_operacao = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Relaciona com a Categoria
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.valor} ({self.data_operacao})"

