# Generated by Django 3.2.12 on 2022-09-08 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSistemaContable', '0003_alter_usuario_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='imagen',
            field=models.ImageField(default='/static/images/perfil/default.png', max_length=200, upload_to='static/images/perfil/', verbose_name='Imagen de perfil'),
        ),
    ]