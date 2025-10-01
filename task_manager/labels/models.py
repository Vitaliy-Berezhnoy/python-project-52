from django.db.models import Model, CharField, DateTimeField
from django.utils.translation import gettext_lazy as _


class Label(Model):
    name = CharField(max_length=100, unique=True, verbose_name=_('Name'))
    created_at = DateTimeField(auto_now_add=True,verbose_name=_('Created at'))
    updated_at = DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
        db_table = 'labels'
        ordering = ['name']

    def __str__(self):
        return self.name
