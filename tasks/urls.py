from django.urls import path

from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskCommentCreateView,
    TaskListView,
    TaskUpdateView,
)

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/comments/', TaskCommentCreateView.as_view(), name='task_comment_create'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
