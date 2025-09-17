from django.db import models

# Create your models here.
class Pagante(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False)
    ordem = models.IntegerField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.nome
    