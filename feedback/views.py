from django.shortcuts import render
from .models import Feedback , Disciplina
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import  redirect, get_object_or_404
from django.views import View
from django.db.models import Avg
class HomeView(View):
    def index(request):
        if request.user.is_authenticated:  
            disciplinas = Disciplina.objects.all()  
            return render(request, 'pages/lista-disciplina.html', {'disciplinas': disciplinas})
        else:
            disciplinas = Disciplina.objects.all()  
            return render(request, 'pages/home.html', {'disciplinas': disciplinas})
        
@login_required(login_url='login')
def disciplina_list_view(request):
    disciplinas = Disciplina.objects.all()
    disciplinas_com_media = []

    for disciplina in disciplinas:
        media = Feedback.objects.filter(disciplina=disciplina).aggregate(
            media_nota=Avg('nota'))['media_nota']
        disciplinas_com_media.append({
            'disciplina': disciplina,
            'media': round(media, 1) if media is not None else 'Sem notas'
        })

    return render(request, 'pages/lista-disciplina.html', {'disciplinas_com_media': disciplinas_com_media})

@login_required(login_url='login')
def disciplina_detalhes_view(request, pk):
    disciplinas = Disciplina.objects.get(pk=pk)
    feedbacks = Feedback.objects.filter(disciplina=disciplinas).order_by('-id')
    usuario_feedback = Feedback.objects.filter(disciplina=disciplinas, usuario=request.user).first()
    media = feedbacks.aggregate(media_nota=Avg('nota'))['media_nota']

    return render(request, 'pages/detalhe-disciplina.html', {
        'disciplinas': disciplinas,
        'feedbacks': feedbacks,
        'usuario_feedback': usuario_feedback,
        'media': round(media, 1) if media is not None else None
    })
 
@login_required(login_url='login')
def feedback_create_view(request, pk):
    disciplinas = get_object_or_404(Disciplina, pk=pk)
    try:
        feedback_existente = Feedback.objects.get(disciplina=disciplinas, usuario=request.user)
        return redirect('editar_feedback', pk=feedback_existente.pk)
    except Feedback.DoesNotExist:
        if request.method == 'POST':
            nota = request.POST.get('nota')
            comentario = request.POST.get('comentario')

            if not nota:
                erro_mensagem = "Por favor, preencha a nota."
                return render(request, 'pages/formulario-disciplina.html', {'erro_mensagem': erro_mensagem, 'disciplina_pk': pk})

            try:
                nota = int(nota)
                if nota < 1 or nota > 5:
                    erro_mensagem = "A nota deve ser um número entre 1 e 5."
                    return render(request, 'pages/formulario-disciplina.html', {'erro_mensagem': erro_mensagem, 'disciplina_pk': pk})
            except ValueError:
                erro_mensagem = "A nota deve ser um número válido."
                return render(request, 'pages/formulario-disciplina.html', {'erro_mensagem': erro_mensagem, 'disciplina_pk': pk})

            feedback = Feedback(disciplina=disciplinas, usuario=request.user, nota=nota, comentario=comentario)
            feedback.save()
            return redirect('detalhe_disciplina', pk=pk)
        else:
            return render(request, 'pages/formulario-disciplina.html', {'disciplina_pk': pk})
        
@login_required(login_url='login')
def feedback_edit_view(request, pk):
    feedbacks = get_object_or_404(Feedback, pk=pk, usuario=request.user)
    disciplina_pk = feedbacks.disciplina_id
    if request.method == 'POST':
        nota = request.POST.get('nota')
        comentario = request.POST.get('comentario')

        if not nota:
            erro_mensagem = "Por favor, preencha a nota"
            return render(request, 'pages/editar-feedback-disciplina.html', {'erro_mensagem': erro_mensagem, 'feedback': feedbacks, 'disciplina_pk': disciplina_pk})

        try:
            nota = int(nota)
            if nota < 1 or nota > 5:
                erro_mensagem = "A nota deve ser um número entre 1 e 5."
                return render(request, 'pages/editar-feedback-disciplina.html', {'erro_mensagem': erro_mensagem, 'feedback': feedbacks, 'disciplina_pk': disciplina_pk})
        except ValueError:
            erro_mensagem = "A nota deve ser um número válido."
            return render(request, 'pages/editar-feedback-disciplina.html', {'erro_mensagem': erro_mensagem, 'feedback': feedbacks, 'disciplina_pk': disciplina_pk})

        feedbacks.nota = nota
        feedbacks.comentario = comentario
        feedbacks.save()
        return redirect('detalhe_disciplina', pk=disciplina_pk)

    return render(request, 'pages/editar-feedback-disciplina.html', {'feedback': feedbacks, 'disciplina_pk': disciplina_pk})

@login_required(login_url='login')
def feedback_delete_view(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk, usuario=request.user)
    disciplina_pk = feedback.disciplina_id
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, "Feedback excluído com sucesso!")
        return redirect('detalhe_disciplina', pk=disciplina_pk)
    else:
        return redirect('detalhe_disciplina', pk=disciplina_pk)
