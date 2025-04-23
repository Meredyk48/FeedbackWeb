from django.contrib import admin
from .models import Feedback, Disciplina

@admin.register(Disciplina)
class AdminDisciplina(admin.ModelAdmin):
    list_display = ('nome', 'professor')
    list_filter = ('nome', 'professor')

@admin.register(Feedback)
class AdminFeedback(admin.ModelAdmin):
    list_display = ("disciplina","nota","comentario")
    list_filter = ("disciplina","nota")