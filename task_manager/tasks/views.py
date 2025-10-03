from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.contrib import messages
from django_filters.views import FilterView
from .models import Task
from .forms import TaskForm
from .filters import TaskFilter


class TasksListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('status', 'author', 'executor').prefetch_related('labels')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return super().get_queryset().select_related('status', 'author', 'executor').prefetch_related('labels')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        """Устанавливаем автора задачи автоматически"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully updated')


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully deleted')

    def test_func(self):
        """Проверяем, что пользователь - автор задачи"""
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        """Обработка случая, когда пользователь не автор"""
        messages.error(self.request, _('Only the author can delete a task'))
        return redirect('tasks:tasks')