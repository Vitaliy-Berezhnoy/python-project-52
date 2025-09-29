from django.forms import ModelForm,TextInput
from django.utils.translation import gettext_lazy as _
from .models import Status


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': _('Name')}
        widgets = {'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')})}