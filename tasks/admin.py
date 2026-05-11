from django.contrib import admin

from .models import Task, TaskComment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'owner', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at', 'media')
    list_filter = ('created_at',)
    search_fields = ('text', 'task__title', 'author__username')
