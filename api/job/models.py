from django.db import models

JOB_STATUS_CHOICES = [
    ('OPEN', 'OPEN'),
    ('CLOSED', 'CLOSED'),
    ('PENDING', 'PENDING')
]


class Job(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=25, choices=JOB_STATUS_CHOICES)
    skill = models.ForeignKey(to='skill.Skill', on_delete=models.PROTECT)
    opinions = models.ManyToManyField(to='candidate.Candidate', through='Opinion')

    def __str__(self):
        return self.title


class Opinion(models.Model):

    class Meta:
        unique_together = ['job', 'candidate']

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey('candidate.Candidate', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField()
