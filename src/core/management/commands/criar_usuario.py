from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Cria o usuário Thiago caso ele ainda não exista'

    def handle(self, *args, **options):
        User = get_user_model()

        username = 'Thiago'
        password = '1234'
        email = 'thiago@example.com'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )

        if created:
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    'Usuário Thiago criado com sucesso.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Usuário Thiago já existe.'
                )
            )