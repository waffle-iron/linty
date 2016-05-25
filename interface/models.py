from django.db import models


class Result(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    base_dir = models.TextField()
