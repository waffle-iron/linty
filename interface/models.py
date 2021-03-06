from django.contrib.auth.models import User
from django.db import models

from interface.utils import get_github


class Repo(models.Model):
    user = models.ForeignKey(User, related_name='repos')
    full_name = models.TextField()
    webhook_id = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, using=None, keep_parents=False):
        g = get_github(self.user)
        hook = g.get_repo(self.full_name).get_hook(self.webhook_id)
        hook.delete()

        super(Repo, self).delete(using=using, keep_parents=keep_parents)

    class Meta:
        ordering = ['full_name']


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
    result = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def get_duration(self):
        delta = self.finished_at - self.created_at
        s = delta.seconds
        minutes, seconds = divmod(s, 60)
        return '%sm:%ss' % (minutes, seconds)

    class Meta:
        ordering = ['-created_at']
