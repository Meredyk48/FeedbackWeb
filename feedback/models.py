from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User



class Disciplina(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    professor = models.CharField(max_length=200, verbose_name="Professor")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descricao")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ["nome"]


class Feedback(models.Model):
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        verbose_name="Disciplina"
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nota = models.IntegerField(
        verbose_name="Nota",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.CharField(max_length=200, verbose_name="Comentario")
    
    def __str__(self):
        return self.comentario
    
    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ["-id"]  
        unique_together = ('disciplina', 'usuario')  

