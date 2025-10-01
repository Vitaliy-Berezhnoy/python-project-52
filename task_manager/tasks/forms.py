from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Description'),
                'rows': 4
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'executor': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поле executor необязательным
        self.fields['executor'].required = False
        self.fields['executor'].empty_label = _('Not selected')

        # Оптимизируем queryset для исполнителей
        self.fields['executor'].queryset = User.objects.all().order_by('username')
        self.fields['status'].queryset = Status.objects.all().order_by('name')

    def clean_name(self):
        """Валидация имени задачи"""
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError(_('Task name must be at least 2 characters long'))
        return name