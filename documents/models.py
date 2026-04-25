from django.db import models
from users.models import User


class Document(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        STORED = 'stored', 'Stored'
        FAILED = 'failed', 'Failed'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(help_text="Size in bytes")
    minio_path = models.CharField(max_length=500)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documents'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.uploaded_by}"