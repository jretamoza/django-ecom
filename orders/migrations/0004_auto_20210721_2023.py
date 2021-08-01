# Generated by Django 3.1 on 2021-07-21 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0003_auto_20210711_1432'),
        ('orders', '0003_auto_20210721_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='tienda.Variation'),
        ),
    ]
