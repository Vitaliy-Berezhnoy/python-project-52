from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.models import User
from task_manager.users.forms import UserRegistrationForm, UserUpdateForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib import messages


class UserPermissionMixin(AccessMixin):
    permission_message = _('You do not have permission to perform this action.')
    redirect_url = 'users'

    def dispatch(self, request, *args, **kwargs):
        # noinspection PyUnresolvedReferences
        if self.request.user != self.get_object():
            messages.error(request, self.permission_message)
            return redirect(self.redirect_url)
        # noinspection PyUnresolvedReferences
        return super().dispatch(request, *args, **kwargs)


class UsersIndexView(ListView):
    model = User  # Модель для отображения
    template_name = 'users/index.html'  # Шаблон
    context_object_name = 'users'  # Имя переменной в шаблоне
    paginate_by = 10  # Пагинация по 10 элементов

class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/new_user.html'
    success_url = reverse_lazy('login')
    success_message = _("The user has been successfully registered")

class UserUpdateView(LoginRequiredMixin, UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _("The user has been successfully updated")
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit User')
        return context


class UserDeleteView(LoginRequiredMixin, UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _("The user has been successfully deleted")
    permission_message = _('You do not have permission to delete another user.')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete User')
        return context
