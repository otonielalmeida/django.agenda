# Generated by Django 4.0.1 on 2022-01-09 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contatos', '0003_contato_mostrar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contato',
            old_name='mostrar',
            new_name='visivel',
        ),
    ]
