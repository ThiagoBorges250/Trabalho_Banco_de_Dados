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


class MatriculaForm(forms.ModelForm):
    data_matricula = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Data da Matrícula'
    )

    class Meta:
        model = Matricula
        fields = ['fk_id_aluno', 'fk_id_disciplina', 'data_matricula', 'nota1', 'nota2', 'nota3']
        labels = {
            'fk_id_aluno': 'Aluno',
            'fk_id_disciplina': 'Disciplina',
            'nota1': 'Nota 1 (0 a 10)',
            'nota2': 'Nota 2 (0 a 10)',
            'nota3': 'Nota 3 (0 a 10)',
        }
        widgets = {
            'fk_id_aluno': forms.Select(attrs={'class': 'form-select'}),
            'fk_id_disciplina': forms.Select(attrs={'class': 'form-select'}),
            'nota1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '10', 'placeholder': '0.0'}),
            'nota2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '10', 'placeholder': '0.0'}),
            'nota3': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '10', 'placeholder': '0.0'}),
        }


class MatriculaNotaForm(forms.ModelForm):
    """Formulário para lançar as 3 notas — média e status são calculados automaticamente."""

    class Meta:
        model = Matricula
        fields = ['nota1', 'nota2', 'nota3']
        labels = {
            'nota1': 'Nota 1 (0 a 10)',
            'nota2': 'Nota 2 (0 a 10)',
            'nota3': 'Nota 3 (0 a 10)',
        }
        widgets = {
            'nota1': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '10', 'placeholder': '0.0'
            }),
            'nota2': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '10', 'placeholder': '0.0'
            }),
            'nota3': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '10', 'placeholder': '0.0'
            }),
        }
        help_texts = {
            'nota1': 'Primeira avaliação',
            'nota2': 'Segunda avaliação',
            'nota3': 'Terceira avaliação',
        }
