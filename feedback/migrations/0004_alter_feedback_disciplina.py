# Generated by Django 5.2 on 2025-04-15 00:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_alter_feedback_options_remove_disciplina_feedback_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='disciplina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.disciplina', verbose_name='Disciplina'),
        ),
    ]
