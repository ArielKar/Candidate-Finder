from django.db import models


class Candidate(models.Model):
    title = models.CharField(max_length=100)
    skills = models.ManyToManyField(to='skill.Skill')
    notes = models.ManyToManyField(to='job.Job', through='Note')

    def __str__(self):
        return self.title


class Note(models.Model):
    job = models.ForeignKey('job.Job', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    note = models.CharField(max_length=255)
