# Generated by Django 3.1 on 2021-07-24 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Cuenta', 'verbose_name_plural': 'Cuentas'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Perfil de usuario', 'verbose_name_plural': 'Perfiles usuarios'},
        ),
    ]
