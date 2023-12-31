# Generated by Django 4.2 on 2023-11-18 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Макс 150 символов', max_length=150, verbose_name='Имя')),
                ('is_published', models.BooleanField(default=True, verbose_name='В меню')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Макс 150 символов', max_length=150, verbose_name='Имя')),
                ('is_private', models.BooleanField(default=True, verbose_name='Забронирован')),
            ],
            options={
                'verbose_name': 'Столик',
                'verbose_name_plural': 'Столики',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Макс 150 символов', max_length=150, verbose_name='Имя')),
                ('is_published', models.BooleanField(default=True, verbose_name='В меню')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Макс 150 символов', max_length=150, verbose_name='Имя')),
                ('is_published', models.BooleanField(default=True, verbose_name='В меню')),
                ('text', models.TextField(help_text=('Минимум два слова. Обязательно содержится ', 'слово превосходно или роскошно'), verbose_name='Описание')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.category', verbose_name='Категория')),
                ('tags', models.ManyToManyField(related_name='items', to='core.tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
    ]
