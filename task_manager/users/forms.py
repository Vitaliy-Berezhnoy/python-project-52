from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, TextInput
from django.utils.translation import gettext_lazy as _

from .models import User


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Режим редактирования
        if self.instance.pk:
            #  self.fields['username'].required = False
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    password1 = CharField(
        label=_("Password"),
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Password")}
        ),
        help_text=_("Your password must contain at least 3 characters."),
    )

    password2 = CharField(
        label=_("Password confirmation"),
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Password confirmation"),
            }
        ),
        help_text=_("Please enter the password again to confirm."),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Если это редактирование и username не изменился - пропускаем проверку
        if self.instance.pk and username == self.instance.username:
            return username
        # В остальных случаях используем стандартную валидацию
        return super().clean_username()

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if self.instance.pk and not password1:
            return password1

        if len(password1) < 3:
            raise ValidationError(
                _("Password must be at least 3 characters long")
            )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if self.instance.pk and not password1 and not password2:
            return password2
        if password1 != password2:
            raise ValidationError(_("The entered passwords do not match."))
        return password2

    def save(self, commit=True):
        # Вызываем родительский save() с commit=False
        # Это создает объект пользователя в памяти, но НЕ сохраняет в БД
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        # Если пароль не введен и это редактирование - НЕ меняем пароль
        if self.instance.pk and not password:
            # Получаем текущего пользователя из базы и копируем пароль
            current_user = User.objects.get(pk=self.instance.pk)
            user.password = current_user.password
        else:
            user.set_password(password)

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2"
        ]
        labels = {
            "first_name": _("Name"),
            "last_name": _("Surname"),
            "username": _("Username"),
        }
        widgets = {
            "first_name": TextInput(
                attrs={"class": "form-control", "placeholder": _("Name")}
            ),
            "last_name": TextInput(
                attrs={"class": "form-control", "placeholder": _("Surname")}
            ),
            "username": TextInput(
                attrs={"class": "form-control", "placeholder": _("Username")}
            ),
        }
        help_texts = {
            "username": _(
                "Required field. No more than 150 characters. "
                "Only letters, numbers, and symbols @/./+/-/_."
            )
        }