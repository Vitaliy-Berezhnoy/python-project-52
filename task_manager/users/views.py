from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import UserRegistrationForm
from task_manager.users.models import User


class UserPermissionMixin(AccessMixin):
    permission_message = _("You don't have the rights to change another user")
    redirect_url = "users"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            messages.error(request, self.permission_message)
            return redirect(self.redirect_url)           # redirect_url ?
        return super().dispatch(request, *args, **kwargs)


class UsersIndexView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    paginate_by = 10
    ordering = ["id"]


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/new_user.html"
    success_url = reverse_lazy("login")
    success_message = _("The user has been successfully registered")
    form_title = _("Registration")
    form_submit = _("Register")


class UserUpdateView(
    LoginRequiredMixin, UserPermissionMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users")
    success_message = _("The user has been successfully updated")
    login_url = reverse_lazy("login")
    form_title = _("Edit User")
    form_submit = _("To change")


class UserDeleteView(
    LoginRequiredMixin, UserPermissionMixin, SuccessMessageMixin, DeleteView
):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users")
    success_message = _("The user has been successfully deleted")
    permission_message = _("You do not have permission to delete another user.")
    login_url = reverse_lazy("login")