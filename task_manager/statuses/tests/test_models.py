from django.test import TestCase
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _


class StatusModelTest(TestCase):
    def setUp(self):
        """Подготовка тестовых данных - создаем тестовый статус"""
        self.status_data = {
            'name': 'новый'
        }

    def test_create_status(self):
        """Проверяет, что статус создается с правильными атрибутами"""
        status = Status.objects.create(**self.status_data)
        self.assertEqual(status.name, 'новый')
        self.assertIsNotNone(status.created_at)
        self.assertIsNotNone(status.updated_at)

    def test_status_string_representation(self):
        """Проверяет, что строковое представление статуса возвращает его имя"""
        status = Status.objects.create(**self.status_data)
        self.assertEqual(str(status), 'новый')

    def test_status_verbose_names(self):
        """Проверяет, что verbose_name и verbose_name_plural настроены правильно"""
        self.assertEqual(Status._meta.verbose_name, _('Status'))
        self.assertEqual(Status._meta.verbose_name_plural, _('Statuses'))

    def test_status_table_name(self):
        """Проверяет, что имя таблицы в базе данных установлено правильно"""
        self.assertEqual(Status._meta.db_table, 'statuses')

    def test_status_unique_name(self):
        """Проверяет, что имя статуса должно быть уникальным"""
        Status.objects.create(**self.status_data)
        # Попытка создать статус с таким же именем должна вызвать ошибку
        with self.assertRaises(Exception):
            Status.objects.create(name='новый')

    def test_status_name_max_length(self):
        """Проверяет максимальную длину поля name (100 символов)"""
        status = Status.objects.create(**self.status_data)
        max_length = status._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_status_ordering(self):
        """Проверяет порядок статусов по умолчанию (по времени создания)"""
        status1 = Status.objects.create(name='в работе')
        status2 = Status.objects.create(name='завершен')

        # Статусы должны быть упорядочены по created_at (самые старые первыми)
        all_statuses = Status.objects.all()
        self.assertEqual(all_statuses[0], status1)
        self.assertEqual(all_statuses[1], status2)

    def test_status_fields_exist(self):
        """Проверяет, что у модели есть все необходимые поля"""
        status = Status.objects.create(**self.status_data)

        # Проверяем наличие полей
        self.assertTrue(hasattr(status, 'id'))
        self.assertTrue(hasattr(status, 'name'))
        self.assertTrue(hasattr(status, 'created_at'))
        self.assertTrue(hasattr(status, 'updated_at'))

    def test_status_field_attributes(self):
        """Проверяет атрибуты полей модели"""
        name_field = Status._meta.get_field('name')

        # Проверяем атрибуты поля name
        self.assertTrue(name_field.unique)
        self.assertEqual(name_field.max_length, 100)
        self.assertEqual(name_field.verbose_name, _('Name'))

    def test_status_created_updated_auto_now(self):
        """Проверяет, что created_at и updated_at автоматически устанавливаются"""
        status = Status.objects.create(name='тестовый статус')

        # Поля должны быть установлены автоматически
        self.assertIsNotNone(status.created_at)
        self.assertIsNotNone(status.updated_at)

        # При сохранении updated_at должен обновляться
        old_updated = status.updated_at
        status.name = 'обновленный статус'
        status.save()
        status.refresh_from_db()

        self.assertNotEqual(status.updated_at, old_updated)