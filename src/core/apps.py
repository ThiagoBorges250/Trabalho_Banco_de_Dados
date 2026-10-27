from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Sempre que alunos, professores, disciplinas ou matriculas mudam,
        # o cache do Redis e invalidado.
        from django.db.models.signals import post_delete, post_save

        from . import cache_utils
        from .models import Aluno, Disciplina, Matricula, Professor

        def _invalidar(sender, **kwargs):
            cache_utils.invalidar()

        for modelo in (Aluno, Professor, Disciplina, Matricula):
            post_save.connect(_invalidar, sender=modelo, weak=False,
                              dispatch_uid=f'inv_save_{modelo.__name__}')
            post_delete.connect(_invalidar, sender=modelo, weak=False,
                                dispatch_uid=f'inv_del_{modelo.__name__}')
