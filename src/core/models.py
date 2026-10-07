from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Aluno(models.Model):
    id_aluno = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=9, blank=True, null=True)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField()

    class Meta:
        db_table = 'alunos'
        managed = False
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Professor(models.Model):
    id_professor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=9, blank=True, null=True)
    data_nascimento = models.DateField()
    especialidade = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'professores'
        managed = False
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    nome_disciplina = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    fk_id_professor = models.ForeignKey(
        Professor,
        on_delete=models.RESTRICT,
        db_column='fk_id_professor',
        related_name='disciplinas'
    )

    class Meta:
        db_table = 'disciplinas'
        managed = False
        ordering = ['nome_disciplina']

    def __str__(self):
        return self.nome_disciplina


STATUS_CHOICES = [
    ('aprovado', 'Aprovado'),
    ('reprovado', 'Reprovado'),
    ('matriculado', 'Matriculado'),
    ('cancelado', 'Cancelado'),
]

MEDIA_MINIMA = 7.0


class Matricula(models.Model):
    """
    Tabela `matricula` criada pelo script SQL.
    A matrícula é criada pela procedure `realizar_matricula`;
    as notas são lançadas pela aba Notas.
    """
    id_matricula = models.AutoField(primary_key=True)

    fk_id_aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE,
        db_column='fk_id_aluno', related_name='matriculas'
    )
    fk_id_disciplina = models.ForeignKey(
        Disciplina, on_delete=models.CASCADE,
        db_column='fk_id_disciplina', related_name='matriculas'
    )
    data_matricula = models.DateField()

    nota1 = models.FloatField(null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name='Nota 1')
    nota2 = models.FloatField(null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name='Nota 2')
    nota3 = models.FloatField(null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name='Nota 3')

    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              null=True, blank=True)

    class Meta:
        db_table = 'matricula'
        managed = False
        unique_together = ('fk_id_aluno', 'fk_id_disciplina')
        ordering = ['-data_matricula']

    @property
    def media(self):
        if self.nota1 is not None and self.nota2 is not None and self.nota3 is not None:
            return round((self.nota1 + self.nota2 + self.nota3) / 3, 2)
        return None

    def save(self, *args, **kwargs):
        if self.status != 'cancelado':
            if self.nota1 is None and self.nota2 is None and self.nota3 is None:
                self.status = 'matriculado'
            elif self.nota1 is not None and self.nota2 is not None and self.nota3 is not None:
                self.status = 'aprovado' if self.media >= MEDIA_MINIMA else 'reprovado'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fk_id_aluno} — {self.fk_id_disciplina}"

