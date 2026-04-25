from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        EDITOR = 'editor', 'Editor'
        VIEWER = 'viewer', 'Viewer'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VIEWER
    )

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_editor(self):
        return self.role == self.Role.EDITOR

    def is_viewer(self):
        return self.role == self.Role.VIEWER

    def __str__(self):
        return f"{self.username} ({self.role})"