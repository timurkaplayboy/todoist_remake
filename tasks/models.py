from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):

    class Status(models.TextChoices):
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskComment(models.Model):
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
    VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm')

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='task_comments'
    )
    text = models.TextField(blank=True)
    media = models.FileField(
        upload_to='task_comments/%Y/%m/%d/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.task}'

    @property
    def media_name(self):
        if not self.media:
            return ''
        return self.media.name.rsplit('/', 1)[-1]

    @property
    def is_image(self):
        return bool(self.media and self.media.name.lower().endswith(self.IMAGE_EXTENSIONS))

    @property
    def is_video(self):
        return bool(self.media and self.media.name.lower().endswith(self.VIDEO_EXTENSIONS))
