from django.contrib import admin
from .models import Aluno, Professor, Disciplina, Matricula

admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Disciplina)
admin.site.register(Matricula)

admin.site.site_header = 'Gerente de Notas'
admin.site.site_title = 'Gerente de Notas'
