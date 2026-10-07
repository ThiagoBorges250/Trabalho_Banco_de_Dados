from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db import connection, DatabaseError
from django.urls import reverse

from .models import Aluno, Professor, Disciplina, Matricula, MEDIA_MINIMA

from .forms import (
    AlunoForm,
    ProfessorForm,
    DisciplinaForm,
    MatriculaForm,
    MatriculaNotaForm
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
        alunos = alunos.filter(
            Q(nome__icontains=q) |
            Q(cpf__icontains=q)
        )

    alunos = alunos.order_by(order)

    return render(
        request,
        'core/alunos/list.html',
        {
            'alunos': alunos,
            'q': q,
            'order': order
        }
    )


@login_required
def aluno_create(request):
    form = AlunoForm(request.POST or None)

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Aluno cadastrado com sucesso.'
        )

        return redirect('aluno_list')

    return render(
        request,
        'core/alunos/form.html',
        {
            'form': form,
            'titulo': 'Cadastrar Aluno'
        }
    )


@login_required
def aluno_update(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)

    form = AlunoForm(
        request.POST or None,
        instance=aluno
    )

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Aluno atualizado com sucesso.'
        )

        return redirect('aluno_list')

    return render(
        request,
        'core/alunos/form.html',
        {
            'form': form,
            'titulo': 'Atualizar Aluno',
            'obj': aluno
        }
    )


@login_required
def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)

    if request.method == 'POST':
        aluno.delete()

        messages.success(
            request,
            'Aluno excluído com sucesso.'
        )

        return redirect('aluno_list')

    return render(
        request,
        'core/confirm_delete.html',
        {
            'obj': aluno,
            'tipo': 'Aluno',
            'cancel_url': reverse('aluno_list')
        }
    )


# ─── PROFESSORES ─────────────────────────────────────────────────────────────

@login_required
def professor_list(request):
    q = request.GET.get('q', '')
    order = request.GET.get('order', 'nome')

    professores = Professor.objects.all()

    if q:
        professores = professores.filter(
            Q(nome__icontains=q) |
            Q(especialidade__icontains=q)
        )

    professores = professores.order_by(order)

    return render(
        request,
        'core/professores/list.html',
        {
            'professores': professores,
            'q': q,
            'order': order
        }
    )


@login_required
def professor_create(request):
    form = ProfessorForm(request.POST or None)

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Professor cadastrado com sucesso.'
        )

        return redirect('professor_list')

    return render(
        request,
        'core/professores/form.html',
        {
            'form': form,
            'titulo': 'Cadastrar Professor'
        }
    )


@login_required
def professor_update(request, pk):
    professor = get_object_or_404(
        Professor,
        pk=pk
    )

    form = ProfessorForm(
        request.POST or None,
        instance=professor
    )

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Professor atualizado com sucesso.'
        )

        return redirect('professor_list')

    return render(
        request,
        'core/professores/form.html',
        {
            'form': form,
            'titulo': 'Atualizar Professor',
            'obj': professor
        }
    )


@login_required
def professor_delete(request, pk):
    professor = get_object_or_404(
        Professor,
        pk=pk
    )

    if request.method == 'POST':
        professor.delete()

        messages.success(
            request,
            'Professor excluído com sucesso.'
        )

        return redirect('professor_list')

    return render(
        request,
        'core/confirm_delete.html',
        {
            'obj': professor,
            'tipo': 'Professor',
            'cancel_url': reverse('professor_list')
        }
    )


# ─── DISCIPLINAS ─────────────────────────────────────────────────────────────

@login_required
def disciplina_list(request):
    q = request.GET.get('q', '')
    order = request.GET.get(
        'order',
        'nome_disciplina'
    )

    disciplinas = Disciplina.objects.select_related(
        'fk_id_professor'
    )

    if q:
        disciplinas = disciplinas.filter(
            Q(nome_disciplina__icontains=q) |
            Q(fk_id_professor__nome__icontains=q)
        )

    disciplinas = disciplinas.order_by(order)

    return render(
        request,
        'core/disciplinas/list.html',
        {
            'disciplinas': disciplinas,
            'q': q,
            'order': order
        }
    )


@login_required
def disciplina_create(request):
    form = DisciplinaForm(request.POST or None)

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Disciplina cadastrada com sucesso.'
        )

        return redirect('disciplina_list')

    return render(
        request,
        'core/disciplinas/form.html',
        {
            'form': form,
            'titulo': 'Cadastrar Disciplina'
        }
    )


@login_required
def disciplina_update(request, pk):
    disciplina = get_object_or_404(
        Disciplina,
        pk=pk
    )

    form = DisciplinaForm(
        request.POST or None,
        instance=disciplina
    )

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Disciplina atualizada com sucesso.'
        )

        return redirect('disciplina_list')

    return render(
        request,
        'core/disciplinas/form.html',
        {
            'form': form,
            'titulo': 'Atualizar Disciplina',
            'obj': disciplina
        }
    )


@login_required
def disciplina_delete(request, pk):
    disciplina = get_object_or_404(
        Disciplina,
        pk=pk
    )

    if request.method == 'POST':
        disciplina.delete()

        messages.success(
            request,
            'Disciplina excluída com sucesso.'
        )

        return redirect('disciplina_list')

    return render(
        request,
        'core/confirm_delete.html',
        {
            'obj': disciplina,
            'tipo': 'Disciplina',
            'cancel_url': reverse('disciplina_list')
        }
    )


# ─── MATRÍCULAS ──────────────────────────────────────────────────────────────

@login_required
def matricula_list(request):
    q = request.GET.get('q', '')
    status_filtro = request.GET.get('status', '')
    order = request.GET.get(
        'order',
        '-data_matricula'
    )

    matriculas = Matricula.objects.select_related(
        'fk_id_aluno',
        'fk_id_disciplina',
        'fk_id_disciplina__fk_id_professor'
    )

    if q:
        matriculas = matriculas.filter(
            Q(fk_id_aluno__nome__icontains=q) |
            Q(fk_id_disciplina__nome_disciplina__icontains=q)
        )

    if status_filtro:
        matriculas = matriculas.filter(
            status=status_filtro
        )

    matriculas = matriculas.order_by(order)

    return render(
        request,
        'core/matriculas/list.html',
        {
            'matriculas': matriculas,
            'q': q,
            'status_filtro': status_filtro,
            'order': order
        }
    )


def _mensagem_erro_banco(exc):
    """
    A Procedure usa RAISE EXCEPTION.
    Retorna somente a primeira linha da mensagem.
    """
    texto = str(exc).strip()

    if texto:
        return texto.splitlines()[0]

    return 'Não foi possível realizar a matrícula.'


@login_required
def matricula_create(request):
    """
    Realiza a matrícula utilizando a Procedure
    realizar_matricula do PostgreSQL.
    """

    form = MatriculaForm(
        request.POST or None
    )

    if request.method == 'POST' and form.is_valid():

        aluno = form.cleaned_data['aluno']
        disciplina = form.cleaned_data['disciplina']

        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    'CALL realizar_matricula(%s, %s);',
                    [
                        aluno.pk,
                        disciplina.pk
                    ]
                )

        except DatabaseError as e:

            messages.error(
                request,
                _mensagem_erro_banco(e)
            )

        else:

            messages.success(
                request,
                'Matrícula realizada com sucesso.'
            )

            return redirect('matricula_list')

    return render(
        request,
        'core/matriculas/form.html',
        {
            'form': form,
            'titulo': 'Matricular Aluno'
        }
    )


@login_required
def matricula_delete(request, pk):
    matricula = get_object_or_404(
        Matricula,
        pk=pk
    )

    if request.method == 'POST':

        matricula.delete()

        messages.success(
            request,
            'Matrícula excluída com sucesso.'
        )

        return redirect('matricula_list')

    return render(
        request,
        'core/confirm_delete.html',
        {
            'obj': matricula,
            'tipo': 'Matrícula',
            'cancel_url': reverse('matricula_list')
        }
    )


# ─── NOTAS ───────────────────────────────────────────────────────────────────

@login_required
def notas_list(request):

    q = request.GET.get('q', '')
    status_filtro = request.GET.get(
        'status',
        ''
    )
    disciplina_id = request.GET.get(
        'disciplina',
        ''
    )
    order = request.GET.get(
        'order',
        'fk_id_aluno__nome'
    )

    notas = Matricula.objects.select_related(
        'fk_id_aluno',
        'fk_id_disciplina',
        'fk_id_disciplina__fk_id_professor'
    ).exclude(
        status='cancelado'
    )

    if q:
        notas = notas.filter(
            Q(fk_id_aluno__nome__icontains=q)
        )

    if status_filtro:
        notas = notas.filter(
            status=status_filtro
        )

    if disciplina_id:
        notas = notas.filter(
            fk_id_disciplina__id_disciplina=disciplina_id
        )

    notas = notas.order_by(order)

    disciplinas = Disciplina.objects.all().order_by(
        'nome_disciplina'
    )

    return render(
        request,
        'core/notas/list.html',
        {
            'notas': notas,
            'q': q,
            'status_filtro': status_filtro,
            'disciplina_id': disciplina_id,
            'order': order,
            'disciplinas': disciplinas
        }
    )


@login_required
def nota_editar(request, pk):

    matricula = get_object_or_404(
        Matricula,
        pk=pk
    )

    form = MatriculaNotaForm(
        request.POST or None,
        instance=matricula
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Notas atualizadas com sucesso.'
        )

        return redirect('notas_list')

    return render(
        request,
        'core/matriculas/nota.html',
        {
            'form': form,
            'mat': matricula
        }
    )


# ─── RELATÓRIOS ──────────────────────────────────────────────────────────────

@login_required
def relatorios(request):

    todas = Matricula.objects.select_related(
        'fk_id_aluno',
        'fk_id_disciplina',
        'fk_id_disciplina__fk_id_professor'
    ).exclude(
        status='cancelado'
    ).order_by(
        'fk_id_aluno__nome'
    )

    aprovados = todas.filter(
        status='aprovado'
    )

    reprovados = todas.filter(
        status='reprovado'
    )

    alunos_sem_matricula = Aluno.objects.filter(
        matriculas__isnull=True
    )

    return render(
        request,
        'core/relatorios/index.html',
        {
            'todas': todas,
            'aprovados': aprovados,
            'reprovados': reprovados,
            'alunos_sem_matricula': alunos_sem_matricula
        }
    )


# ─── VIEW DO POSTGRESQL ──────────────────────────────────────────────────────

@login_required
def relatorio_view(request):

    disciplina_id = request.GET.get(
        'disciplina',
        ''
    )

    with connection.cursor() as cursor:

        # Lista as disciplinas existentes na View
        cursor.execute("""
            SELECT
                id_disciplina,
                disciplina
            FROM vw_relatorio_alunos
            GROUP BY
                id_disciplina,
                disciplina
            ORDER BY
                disciplina;
        """)

        disciplinas = cursor.fetchall()

        # Relatório filtrado
        if disciplina_id:

            cursor.execute("""
                SELECT
                    id_aluno,
                    aluno,
                    disciplina,
                    professor,
                    nota1,
                    nota2,
                    nota3,
                    status,
                    data_matricula
                FROM vw_relatorio_alunos
                WHERE id_disciplina = %s
                ORDER BY aluno;
            """, [disciplina_id])

        # Relatório completo
        else:

            cursor.execute("""
                SELECT
                    id_aluno,
                    aluno,
                    disciplina,
                    professor,
                    nota1,
                    nota2,
                    nota3,
                    status,
                    data_matricula
                FROM vw_relatorio_alunos
                ORDER BY aluno;
            """)

        resultados = cursor.fetchall()

    return render(
        request,
        'core/relatorios/view.html',
        {
            'resultados': resultados,
            'disciplinas': disciplinas,
            'disciplina_id': disciplina_id
        }
    )


# ─── FUNCTION DO POSTGRESQL ──────────────────────────────────────────────────

@login_required
def media_aluno(request):

    alunos = Aluno.objects.all().order_by('nome')

    media = None
    aluno = None
    boletim = []
    aluno_selecionado = request.POST.get('id_aluno') or request.GET.get('aluno')

    if aluno_selecionado and str(aluno_selecionado).isdigit():

        aluno = Aluno.objects.filter(pk=aluno_selecionado).first()

        if aluno:
            # Executa a Function calcular_media_aluno do PostgreSQL
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT calcular_media_aluno(%s);",
                    [aluno.pk]
                )
                resultado = cursor.fetchone()
                if resultado and resultado[0] is not None:
                    media = float(resultado[0])

            boletim = list(
                Matricula.objects.select_related(
                    'fk_id_disciplina',
                    'fk_id_disciplina__fk_id_professor'
                ).filter(
                    fk_id_aluno=aluno
                ).exclude(
                    status='cancelado'
                ).order_by('fk_id_disciplina__nome_disciplina')
            )

    total = len(boletim)
    aprovadas = sum(1 for m in boletim if m.status == 'aprovado')
    reprovadas = sum(1 for m in boletim if m.status == 'reprovado')
    em_curso = total - aprovadas - reprovadas

    if media is None:
        situacao = None
    elif media >= MEDIA_MINIMA:
        situacao = 'aprovado'
    else:
        situacao = 'reprovado'

    return render(
        request,
        'core/relatorios/media.html',
        {
            'alunos': alunos,
            'aluno': aluno,
            'aluno_selecionado': str(aluno_selecionado or ''),
            'media': media,
            'media_pct': int((media or 0) * 10),
            'media_minima': MEDIA_MINIMA,
            'situacao': situacao,
            'boletim': boletim,
            'total': total,
            'aprovadas': aprovadas,
            'reprovadas': reprovadas,
            'em_curso': em_curso,
        }
    )
