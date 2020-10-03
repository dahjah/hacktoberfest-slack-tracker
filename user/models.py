from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    github_username = models.CharField(blank=True, max_length=255)
    slack_username = models.CharField(blank=True, max_length=255)
    slack_id = models.CharField(blank=True, max_length=255)
    watch_for_pull_requests = models.BooleanField(default=False)
    notify_count_in_slack = models.BooleanField(default=False)

    def __str__(self):
        return self.email