# Generated by Django 4.2 on 2023-11-18 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_table_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, help_text='Когда был создан', verbose_name='создан'),
        ),
    ]