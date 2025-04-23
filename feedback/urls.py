from django.urls import path
from . import views
from .views import  HomeView

urlpatterns = [
    path('', HomeView.index, name='home'),
    path('disciplinas', views.disciplina_list_view, name='listagem_disciplina'),
    path('disciplinas/<int:pk>/',views.disciplina_detalhes_view, name='detalhe_disciplina'),
    path('disciplinas/<int:pk>/avaliar/', views.feedback_create_view, name='avaliar'),
    path('disciplinas/<int:pk>/editar/', views.feedback_edit_view, name='editar_feedback'),
    path('feedback/<int:pk>/excluir/', views.feedback_delete_view, name='excluir_feedback')

]