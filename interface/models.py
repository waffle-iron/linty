from django.contrib.auth.models import User
from django.db import models


class Repo(models.Model):
    user = models.ForeignKey(User, related_name='repos')
    full_name = models.TextField()
    webhook_id = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, using=None, keep_parents=False):


        super(Repo, self).delete(using=using, keep_parents=keep_parents)


class Build(models.Model):
    SUCCESS = 'success'
    ERROR = 'error'
    PENDING = 'pending'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (SUCCESS, SUCCESS),
        (ERROR, ERROR),
        (PENDING, PENDING),
        (CANCELLED, CANCELLED)
    )

    repo = models.ForeignKey(Repo)
    ref = models.TextField()
    sha = models.TextField()
    status = models.TextField(choices=STATUS_CHOICES, default=PENDING)
    result = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

