from django.views.generic import ListView
from task_manager.users.models import Users


# Create your views here.
class UsersIndexView(ListView):
    model = Users  # Модель для отображения
    template_name = 'users/index.html'  # Шаблон
    context_object_name = 'users'  # Имя переменной в шаблоне
    paginate_by = 10  # Пагинация по 10 элементов


#def users_index(request):
#    return render(request, 'users/index.html')