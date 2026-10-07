from django import forms
from .models import Aluno, Professor, Disciplina, Matricula


class AlunoForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Data de Nascimento'
    )

    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'email', 'telefone', 'data_nascimento']
        labels = {
            'nome': 'Nome Completo',
            'cpf': 'CPF (somente números)',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000000000', 'maxlength': '11'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '999999999', 'maxlength': '9'}),
        }


class ProfessorForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Data de Nascimento'
    )

    class Meta:
        model = Professor
        fields = ['nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'especialidade']
        labels = {
            'nome': 'Nome Completo',
            'cpf': 'CPF (somente números)',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'especialidade': 'Especialidade',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '9'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome_disciplina', 'carga_horaria', 'fk_id_professor']
        labels = {
            'nome_disciplina': 'Nome da Disciplina',
            'carga_horaria': 'Carga Horária (horas)',
            'fk_id_professor': 'Professor Responsável',
        }
        widgets = {
            'nome_disciplina': forms.TextInput(attrs={'class': 'form-control'}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'fk_id_professor': forms.Select(attrs={'class': 'form-select'}),
        }


class MatriculaForm(forms.Form):
    """Matrícula = escolher aluno + disciplina (feita pela procedure realizar_matricula)."""
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        label='Aluno',
        empty_label='Selecione um aluno',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.all(),
        label='Disciplina',
        empty_label='Selecione uma disciplina',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


class MatriculaNotaForm(forms.ModelForm):
    """Lançamento da nota (aba Notas) — o status é calculado automaticamente."""

    class Meta:
        model = Matricula
        fields = ['nota']
        labels = {'nota': 'Nota (0 a 10)'}
        widgets = {
            'nota': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '10', 'placeholder': '0.0'
            }),
        }
