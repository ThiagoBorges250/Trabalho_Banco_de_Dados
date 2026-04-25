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
        ordering = ['nome_disciplina']

    def __str__(self):
        return self.nome_disciplina


STATUS_CHOICES = [
    ('aprovado', 'Aprovado'),
    ('reprovado', 'Reprovado'),
    ('matriculado', 'Matriculado'),
]

MEDIA_MINIMA = 7.0


class Matricula(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    fk_id_aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        db_column='fk_id_aluno',
        related_name='matriculas'
    )
    fk_id_disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        db_column='fk_id_disciplina',
        related_name='matriculas'
    )
    data_matricula = models.DateField()

    # Três notas individuais
    nota1 = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name='Nota 1'
    )
    nota2 = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name='Nota 2'
    )
    nota3 = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name='Nota 3'
    )

    # Média calculada automaticamente (campo `nota` original preservado)
    nota = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name='Média'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        null=True, blank=True
    )

    class Meta:
        db_table = 'matricula'
        unique_together = ('fk_id_aluno', 'fk_id_disciplina')
        ordering = ['-data_matricula']

    def calcular_media(self):
        """Retorna a média das notas preenchidas, ou None se nenhuma foi informada."""
        valores = [n for n in (self.nota1, self.nota2, self.nota3) if n is not None]
        if not valores:
            return None
        return round(sum(valores) / len(valores), 2)

    def calcular_status(self, media):
        """Retorna o status com base na média (todas as 3 notas preenchidas)."""
        todas_preenchidas = all(
            n is not None for n in (self.nota1, self.nota2, self.nota3)
        )
        if not todas_preenchidas:
            return 'matriculado'
        return 'aprovado' if media >= MEDIA_MINIMA else 'reprovado'

    def save(self, *args, **kwargs):
        media = self.calcular_media()
        self.nota = media
        if media is not None:
            self.status = self.calcular_status(media)
        else:
            self.status = 'matriculado'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fk_id_aluno} — {self.fk_id_disciplina}"
