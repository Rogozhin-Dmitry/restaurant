# Generated by Django 4.2 on 2023-11-18 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_product_dishproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dishproduct',
            name='name',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Макс 150 символов', max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(help_text='Макс 150 символов', max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Макс 150 символов', max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='table',
            name='name',
            field=models.CharField(help_text='Макс 150 символов', max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Макс 150 символов', max_length=150, verbose_name='Название'),
        ),
    ]
