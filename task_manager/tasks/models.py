from django.db.models import Model, CharField, TextField, ForeignKey, PROTECT, DateTimeField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status

User = get_user_model()


class Task(Model):
    name = CharField(max_length=100, verbose_name=_('Name'))
    description = TextField(blank=True, verbose_name=_('Description'))
    status = ForeignKey(
        Status,
        on_delete=PROTECT,
        verbose_name=_('Status')
    )
    author = ForeignKey(
        User,
        on_delete=PROTECT,
        related_name='authored_tasks',
        verbose_name=_('Author')
    )
    executor = ForeignKey(
        User,
        on_delete=PROTECT,
        related_name='assigned_tasks',
        blank=True,
        null=True,
        verbose_name=_('Executor')
    )
    created_at = DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        db_table = 'tasks'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

