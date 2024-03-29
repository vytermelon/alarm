# Generated by Django 4.2.9 on 2024-01-25 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0002_alter_question_day"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="complete",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_text",
            field=models.TextField(default="N/A"),
        ),
    ]
