from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User

from .models import Task


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Status"),
        empty_label=_("Any status"),
    )

    executor = ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_("Executor"),
        empty_label=_("Any executor"),
    )

    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label"),
        empty_label=_("Any label"),
    )

    self_tasks = BooleanFilter(
        method="filter_self_tasks",
        label=_("Only my tasks"),
        widget=CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        executor_filter = self.filters["executor"]
        executor_filter.field.label_from_instance = User.get_full_name

        # Упорядочиваем queryset для выпадающих списков
        self.filters["status"].queryset = Status.objects.all().order_by("name")
        self.filters["executor"].queryset = User.objects.all().order_by(
            "first_name", "last_name", "username"
        )
        self.filters["labels"].queryset = Label.objects.all().order_by("name")
