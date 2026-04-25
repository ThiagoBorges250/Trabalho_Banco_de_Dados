from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matricula',
            name='nota1',
            field=models.FloatField(
                blank=True, null=True,
                verbose_name='Nota 1',
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
            ),
        ),
        migrations.AddField(
            model_name='matricula',
            name='nota2',
            field=models.FloatField(
                blank=True, null=True,
                verbose_name='Nota 2',
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
            ),
        ),
        migrations.AddField(
            model_name='matricula',
            name='nota3',
            field=models.FloatField(
                blank=True, null=True,
                verbose_name='Nota 3',
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
            ),
        ),
    ]
