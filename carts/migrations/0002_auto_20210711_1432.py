# Generated by Django 3.1 on 2021-07-11 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0003_auto_20210711_1432'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'carrito', 'verbose_name_plural': 'carritos'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'items carrito', 'verbose_name_plural': 'items carritos'},
        ),
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='tienda.Variation'),
        ),
    ]