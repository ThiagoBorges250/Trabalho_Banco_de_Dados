from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from .models import Aluno, Professor, Disciplina, Matricula
from .forms import (
    AlunoForm, ProfessorForm, DisciplinaForm,
    MatriculaForm, MatriculaNotaForm
)


# ─── DASHBOARD ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    ctx = {
        'total_alunos': Aluno.objects.count(),
        'total_professores': Professor.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
        'total_matriculas': Matricula.objects.count(),
        'aprovados': Matricula.objects.filter(status='aprovado').count(),
        'reprovados': Matricula.objects.filter(status='reprovado').count(),
        'matriculados': Matricula.objects.filter(status='matriculado').count(),
    }
    return render(request, 'core/dashboard.html', ctx)


# ─── ALUNOS ──────────────────────────────────────────────────────────────────

@login_required
def aluno_list(request):
    q = request.GET.get('q', '')
    order = request.GET.get('order', 'nome')
    alunos = Aluno.objects.all()
    if q:
        alunos = alunos.filter(Q(nome__icontains=q) | Q(cpf__icontains=q))
    alunos = alunos.order_by(order)
    return render(request, 'core/alunos/list.html', {'alunos': alunos, 'q': q, 'order': order})


@login_required
def aluno_create(request):
    form = AlunoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Aluno cadastrado com sucesso.')
        return redirect('aluno_list')
    return render(request, 'core/alunos/form.html', {'form': form, 'titulo': 'Cadastrar Aluno'})


@login_required
def aluno_update(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    form = AlunoForm(request.POST or None, instance=aluno)
    if form.is_valid():
        form.save()
        messages.success(request, 'Aluno atualizado com sucesso.')
        return redirect('aluno_list')
    return render(request, 'core/alunos/form.html', {'form': form, 'titulo': 'Atualizar Aluno', 'obj': aluno})


@login_required
def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso.')
        return redirect('aluno_list')
    return render(request, 'core/confirm_delete.html', {'obj': aluno, 'tipo': 'Aluno', 'cancel_url': reverse('aluno_list')})


# ─── PROFESSORES ─────────────────────────────────────────────────────────────

@login_required
def professor_list(request):
    q = request.GET.get('q', '')
    order = request.GET.get('order', 'nome')
    professores = Professor.objects.all()
    if q:
        professores = professores.filter(Q(nome__icontains=q) | Q(especialidade__icontains=q))
    professores = professores.order_by(order)
    return render(request, 'core/professores/list.html', {'professores': professores, 'q': q, 'order': order})


@login_required
def professor_create(request):
    form = ProfessorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Professor cadastrado com sucesso.')
        return redirect('professor_list')
    return render(request, 'core/professores/form.html', {'form': form, 'titulo': 'Cadastrar Professor'})


@login_required
def professor_update(request, pk):
    prof = get_object_or_404(Professor, pk=pk)
    form = ProfessorForm(request.POST or None, instance=prof)
    if form.is_valid():
        form.save()
        messages.success(request, 'Professor atualizado com sucesso.')
        return redirect('professor_list')
    return render(request, 'core/professores/form.html', {'form': form, 'titulo': 'Atualizar Professor', 'obj': prof})


@login_required
def professor_delete(request, pk):
    prof = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        prof.delete()
        messages.success(request, 'Professor excluído com sucesso.')
        return redirect('professor_list')
    return render(request, 'core/confirm_delete.html', {'obj': prof, 'tipo': 'Professor', 'cancel_url': reverse('professor_list')})


# ─── DISCIPLINAS ─────────────────────────────────────────────────────────────

@login_required
def disciplina_list(request):
    q = request.GET.get('q', '')
    order = request.GET.get('order', 'nome_disciplina')
    disciplinas = Disciplina.objects.select_related('fk_id_professor')
    if q:
        disciplinas = disciplinas.filter(
            Q(nome_disciplina__icontains=q) | Q(fk_id_professor__nome__icontains=q)
        )
    disciplinas = disciplinas.order_by(order)
    return render(request, 'core/disciplinas/list.html', {'disciplinas': disciplinas, 'q': q, 'order': order})


@login_required
def disciplina_create(request):
    form = DisciplinaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Disciplina cadastrada com sucesso.')
        return redirect('disciplina_list')
    return render(request, 'core/disciplinas/form.html', {'form': form, 'titulo': 'Cadastrar Disciplina'})


@login_required
def disciplina_update(request, pk):
    disc = get_object_or_404(Disciplina, pk=pk)
    form = DisciplinaForm(request.POST or None, instance=disc)
    if form.is_valid():
        form.save()
        messages.success(request, 'Disciplina atualizada com sucesso.')
        return redirect('disciplina_list')
    return render(request, 'core/disciplinas/form.html', {'form': form, 'titulo': 'Atualizar Disciplina', 'obj': disc})


@login_required
def disciplina_delete(request, pk):
    disc = get_object_or_404(Disciplina, pk=pk)
    if request.method == 'POST':
        disc.delete()
        messages.success(request, 'Disciplina excluída com sucesso.')
        return redirect('disciplina_list')
    return render(request, 'core/confirm_delete.html', {'obj': disc, 'tipo': 'Disciplina', 'cancel_url': reverse('disciplina_list')})


# ─── MATRÍCULAS ──────────────────────────────────────────────────────────────

@login_required
def matricula_list(request):
    q = request.GET.get('q', '')
    status_filtro = request.GET.get('status', '')
    order = request.GET.get('order', '-data_matricula')
    matriculas = Matricula.objects.select_related('fk_id_aluno', 'fk_id_disciplina')
    if q:
        matriculas = matriculas.filter(
            Q(fk_id_aluno__nome__icontains=q) | Q(fk_id_disciplina__nome_disciplina__icontains=q)
        )
    if status_filtro:
        matriculas = matriculas.filter(status=status_filtro)
    matriculas = matriculas.order_by(order)
    return render(request, 'core/matriculas/list.html', {
        'matriculas': matriculas, 'q': q,
        'status_filtro': status_filtro, 'order': order
    })


@login_required
def matricula_create(request):
    form = MatriculaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Matrícula realizada com sucesso.')
        return redirect('matricula_list')
    return render(request, 'core/matriculas/form.html', {'form': form, 'titulo': 'Matricular Aluno'})


@login_required
def matricula_update(request, pk):
    mat = get_object_or_404(Matricula, pk=pk)
    form = MatriculaForm(request.POST or None, instance=mat)
    if form.is_valid():
        form.save()
        messages.success(request, 'Matrícula atualizada com sucesso.')
        return redirect('matricula_list')
    return render(request, 'core/matriculas/form.html', {'form': form, 'titulo': 'Atualizar Matrícula', 'obj': mat})


@login_required
def matricula_delete(request, pk):
    mat = get_object_or_404(Matricula, pk=pk)
    if request.method == 'POST':
        mat.delete()
        messages.success(request, 'Matrícula excluída com sucesso.')
        return redirect('matricula_list')
    return render(request, 'core/confirm_delete.html', {'obj': mat, 'tipo': 'Matrícula', 'cancel_url': reverse('matricula_list')})


@login_required
def registrar_nota(request, pk):
    mat = get_object_or_404(Matricula, pk=pk)
    form = MatriculaNotaForm(request.POST or None, instance=mat)
    if form.is_valid():
        form.save()
        messages.success(request, 'Nota registrada com sucesso.')
        return redirect('matricula_list')
    return render(request, 'core/matriculas/nota.html', {'form': form, 'mat': mat})


# ─── NOTAS ───────────────────────────────────────────────────────────────────

@login_required
def notas_list(request):
    q              = request.GET.get('q', '')
    status_filtro  = request.GET.get('status', '')
    disciplina_id  = request.GET.get('disciplina', '')
    order          = request.GET.get('order', 'fk_id_aluno__nome')

    notas = Matricula.objects.select_related(
        'fk_id_aluno', 'fk_id_disciplina', 'fk_id_disciplina__fk_id_professor'
    )

    if q:
        notas = notas.filter(Q(fk_id_aluno__nome__icontains=q))
    if status_filtro:
        notas = notas.filter(status=status_filtro)
    if disciplina_id:
        notas = notas.filter(fk_id_disciplina__id_disciplina=disciplina_id)

    notas = notas.order_by(order)

    disciplinas = Disciplina.objects.all().order_by('nome_disciplina')

    return render(request, 'core/notas/list.html', {
        'notas': notas,
        'q': q,
        'status_filtro': status_filtro,
        'disciplina_id': disciplina_id,
        'order': order,
        'disciplinas': disciplinas,
    })


@login_required
def nota_editar(request, pk):
    mat = get_object_or_404(Matricula, pk=pk)
    form = MatriculaNotaForm(request.POST or None, instance=mat)
    if form.is_valid():
        form.save()
        messages.success(request, 'Nota atualizada com sucesso.')
        return redirect('notas_list')
    return render(request, 'core/notas/editar.html', {'form': form, 'mat': mat})


# ─── RELATÓRIOS ──────────────────────────────────────────────────────────────

@login_required
def relatorios(request):
    # Todos os alunos com nota e disciplina (INNER JOIN triplo)
    todas = Matricula.objects.select_related(
        'fk_id_aluno', 'fk_id_disciplina', 'fk_id_disciplina__fk_id_professor'
    ).order_by('fk_id_aluno__nome')

    # Somente aprovados
    aprovados = todas.filter(status='aprovado')

    # Somente reprovados
    reprovados = todas.filter(status='reprovado')

    # LEFT JOIN: alunos sem matrícula
    alunos_sem_matricula = Aluno.objects.filter(matriculas__isnull=True)

    ctx = {
        'todas': todas,
        'aprovados': aprovados,
        'reprovados': reprovados,
        'alunos_sem_matricula': alunos_sem_matricula,
    }
    return render(request, 'core/relatorios/index.html', ctx)
