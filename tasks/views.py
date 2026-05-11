from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView

from .forms import CommentForm, TaskFilterForm, TaskForm
from .mixins import UserIsOwnerMixin
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = (
            Task.objects
            .select_related('owner')
            .annotate(comment_count=Count('comments'))
            .order_by('-created_at')
        )

        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        only_mine = self.request.GET.get('only_mine')

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if only_mine:
            queryset = queryset.filter(owner=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        context['total_tasks'] = Task.objects.count()
        context['my_tasks'] = Task.objects.filter(owner=self.request.user).count()
        context['open_tasks'] = Task.objects.exclude(status=Task.Status.DONE).count()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return (
            Task.objects
            .select_related('owner')
            .prefetch_related('comments__author')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = kwargs.get('comment_form', CommentForm())
        context['comments'] = self.object.comments.select_related('author')
        return context


class TaskCommentCreateView(LoginRequiredMixin, FormView):
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.task = self.task
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        comments = self.task.comments.select_related('author')
        return render(
            self.request,
            'tasks/task_detail.html',
            {'task': self.task, 'comments': comments, 'comment_form': form},
            status=400
        )

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.task.pk})


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
