from django.forms import ModelForm, ValidationError, TextInput, Textarea, Select, SelectMultiple
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels'),
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': _('Description'), 'rows': 4}),
            'status': Select(attrs={'class': 'form-control'}),
            'executor': Select(attrs={'class': 'form-control'}),
            'labels': SelectMultiple(attrs={'class': 'form-control', 'size': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].required = False
        self.fields['executor'].queryset = User.objects.all().order_by('first_name', 'last_name', 'username')
        self.fields['executor'].label_from_instance = User.get_full_name
        self.fields['status'].queryset = Status.objects.all().order_by('name')
        self.fields['labels'].queryset = Label.objects.all().order_by('name')
        self.fields['labels'].required = False

    def clean_name(self):
        """Валидация имени задачи"""
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise ValidationError(_('Task name must be at least 2 characters long'))
        return name