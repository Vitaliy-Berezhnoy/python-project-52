from django.forms import CharField, PasswordInput, TextInput
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from task_manager.users.models import User
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    password1 = CharField(
        label=_("Password"),
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Password")}),
        help_text=_("Your password must contain at least 3 characters.")
    )

    password2 = CharField(
        label=_("Password confirmation"),
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Password confirmation")}),
        help_text=_("Please enter the password again to confirm.")
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 3:
            raise ValidationError(_("Password must be at least 3 characters long"))
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError(_('The entered passwords do not match.'))
        return password2

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        labels = {
            'first_name': _('Name'),
            'last_name': _('Surname'),
            'username': _('Username'),
        }
        widgets={
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Surname')}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')})
        }
        help_text = {'username': _(
            "Required field. No more than 150 characters. Only letters, numbers, and symbols @/./+/-/_."
        )}

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': _('Name'),
            'last_name': _('Surname'),
            'username': _('Username'),
        }

    widgets = {
        'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
        'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Surname')}),
        'username': TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}),
    }

    help_text = {'username': _(
        "Required field. No more than 150 characters. Only letters, numbers, and symbols @/./+/-/_."
    )}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле пароля из формы редактирования
        self.fields.pop('password', None)
