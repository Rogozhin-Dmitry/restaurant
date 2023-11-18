# Generated by Django 4.2 on 2023-11-18 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_order_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='coast',
            field=models.IntegerField(default=1000, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='text',
            field=models.TextField(help_text=('Краткое описание для официанта',), verbose_name='Описание'),
        ),
    ]
