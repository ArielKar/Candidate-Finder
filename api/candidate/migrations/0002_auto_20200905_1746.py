# Generated by Django 3.1.1 on 2020-09-05 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('candidate', '0001_initial'),
        ('skill', '0001_initial'),
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='notes',
            field=models.ManyToManyField(through='candidate.Note', to='job.Job'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='skills',
            field=models.ManyToManyField(to='skill.Skill'),
        ),
    ]
