from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id_aluno', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('telefone', models.CharField(blank=True, max_length=9, null=True)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('data_nascimento', models.DateField()),
            ],
            options={
                'db_table': 'alunos',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id_professor', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('telefone', models.CharField(blank=True, max_length=9, null=True)),
                ('data_nascimento', models.DateField()),
                ('especialidade', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'professores',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id_disciplina', models.AutoField(primary_key=True, serialize=False)),
                ('nome_disciplina', models.CharField(max_length=100)),
                ('carga_horaria', models.IntegerField()),
                ('fk_id_professor', models.ForeignKey(
                    db_column='fk_id_professor',
                    on_delete=django.db.models.deletion.RESTRICT,
                    related_name='disciplinas',
                    to='core.professor',
                )),
            ],
            options={
                'db_table': 'disciplinas',
                'ordering': ['nome_disciplina'],
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id_matricula', models.AutoField(primary_key=True, serialize=False)),
                ('data_matricula', models.DateField()),
                ('nota', models.FloatField(
                    blank=True, null=True,
                    validators=[
                        django.core.validators.MinValueValidator(0.0),
                        django.core.validators.MaxValueValidator(10.0),
                    ],
                )),
                ('status', models.CharField(
                    blank=True,
                    choices=[('aprovado', 'Aprovado'), ('reprovado', 'Reprovado'), ('matriculado', 'Matriculado')],
                    max_length=50, null=True,
                )),
                ('fk_id_aluno', models.ForeignKey(
                    db_column='fk_id_aluno',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='matriculas',
                    to='core.aluno',
                )),
                ('fk_id_disciplina', models.ForeignKey(
                    db_column='fk_id_disciplina',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='matriculas',
                    to='core.disciplina',
                )),
            ],
            options={
                'db_table': 'matricula',
                'ordering': ['-data_matricula'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='matricula',
            unique_together={('fk_id_aluno', 'fk_id_disciplina')},
        ),
    ]
