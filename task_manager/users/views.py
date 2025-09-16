from django.views.generic import ListView, CreateView, UpdateView
#from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.models import User
from task_manager.users.forms import UserRegistrationForm, UserUpdateForm
from django.utils.translation import gettext_lazy as _


# Create your views here.
class UsersIndexView(ListView):
    model = User  # Модель для отображения
    template_name = 'users/index.html'  # Шаблон
    context_object_name = 'users'  # Имя переменной в шаблоне
    paginate_by = 10  # Пагинация по 10 элементов

class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/new_user.html'
    success_url = '/users/'
    message_success = _("The user has been successfully registered")

class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = '/users/'
    message_success = _("The user has been successfully updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit User')
        return context
