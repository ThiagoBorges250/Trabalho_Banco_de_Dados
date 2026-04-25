from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Alunos
    path('alunos/', views.aluno_list, name='aluno_list'),
    path('alunos/novo/', views.aluno_create, name='aluno_create'),
    path('alunos/<int:pk>/editar/', views.aluno_update, name='aluno_update'),
    path('alunos/<int:pk>/excluir/', views.aluno_delete, name='aluno_delete'),

    # Professores
    path('professores/', views.professor_list, name='professor_list'),
    path('professores/novo/', views.professor_create, name='professor_create'),
    path('professores/<int:pk>/editar/', views.professor_update, name='professor_update'),
    path('professores/<int:pk>/excluir/', views.professor_delete, name='professor_delete'),

    # Disciplinas
    path('disciplinas/', views.disciplina_list, name='disciplina_list'),
    path('disciplinas/novo/', views.disciplina_create, name='disciplina_create'),
    path('disciplinas/<int:pk>/editar/', views.disciplina_update, name='disciplina_update'),
    path('disciplinas/<int:pk>/excluir/', views.disciplina_delete, name='disciplina_delete'),

    # Matrículas
    path('matriculas/', views.matricula_list, name='matricula_list'),
    path('matriculas/novo/', views.matricula_create, name='matricula_create'),
    path('matriculas/<int:pk>/editar/', views.matricula_update, name='matricula_update'),
    path('matriculas/<int:pk>/excluir/', views.matricula_delete, name='matricula_delete'),
    path('matriculas/<int:pk>/nota/', views.registrar_nota, name='registrar_nota'),

    # Notas
    path('notas/', views.notas_list, name='notas_list'),
    path('notas/<int:pk>/editar/', views.nota_editar, name='nota_editar'),

    # Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
]
