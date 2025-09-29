from django.db.models import Model, CharField, DateTimeField
from django.utils.translation import gettext_lazy as _


class Status(Model):
    name = CharField(max_length=100, unique=True, verbose_name=_('Name'))
    created_at = DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')
        db_table = 'statuses'

    def __str__(self):
        return self.name
