# Generated by Django 2.2.5 on 2020-05-28 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QAManagement', '0002_question_answer_question_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question_answer',
            old_name='question_answer',
            new_name='question_count',
        ),
    ]
