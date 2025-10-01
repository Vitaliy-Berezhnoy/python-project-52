from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model

User = get_user_model()
TEST_PASSWORD = 'ValidPassword123!'


class LabelModelTest(TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.label_data = {
            'name': 'bug'
        }

    def test_create_label(self):
        """Проверяет, что метка создается с правильными атрибутами"""
        label = Label.objects.create(**self.label_data)
        self.assertEqual(label.name, 'bug')
        self.assertIsNotNone(label.created_at)

    def test_label_string_representation(self):
        """Проверяет, что строковое представление метки возвращает её имя"""
        label = Label.objects.create(**self.label_data)
        self.assertEqual(str(label), 'bug')

    def test_label_verbose_names(self):
        """Проверяет, что verbose_name и verbose_name_plural настроены правильно"""
        self.assertEqual(Label._meta.verbose_name, _('Label'))
        self.assertEqual(Label._meta.verbose_name_plural, _('Labels'))

    def test_label_table_name(self):
        """Проверяет, что имя таблицы в базе данных установлено правильно"""
        self.assertEqual(Label._meta.db_table, 'labels')

    def test_label_ordering(self):
        """Проверяет порядок меток по умолчанию (по имени)"""
        Label.objects.create(name='feature')
        Label.objects.create(name='bug')
        Label.objects.create(name='urgent')

        all_labels = Label.objects.all()
        self.assertEqual(all_labels[0].name, 'bug')  # b
        self.assertEqual(all_labels[1].name, 'feature')  # f
        self.assertEqual(all_labels[2].name, 'urgent')  # u

    def test_label_unique_name(self):
        """Проверяет, что имя метки должно быть уникальным"""
        Label.objects.create(**self.label_data)
        with self.assertRaises(Exception):
            Label.objects.create(name='bug')

    def test_label_name_max_length(self):
        """Проверяет максимальную длину поля name (100 символов)"""
        label = Label.objects.create(**self.label_data)
        max_length = label._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)


class LabelTaskRelationshipTest(TestCase):
    """Тесты для связи многие-ко-многим между метками и задачами"""

    def setUp(self):
        """Подготовка тестовых данных для связи"""
        self.user = User.objects.create_user(
            username='testuser',
            password=TEST_PASSWORD
        )
        self.status = Status.objects.create(name='новый')
        self.bug_label = Label.objects.create(name='bug')
        self.feature_label = Label.objects.create(name='feature')
        self.urgent_label = Label.objects.create(name='urgent')

    def test_task_can_have_multiple_labels(self):
        """Проверяет, что задача может иметь несколько меток"""
        task = Task.objects.create(
            name='Тестовая задача',
            status=self.status,
            author=self.user
        )
        task.labels.add(self.bug_label, self.feature_label)

        self.assertEqual(task.labels.count(), 2)
        self.assertIn(self.bug_label, task.labels.all())
        self.assertIn(self.feature_label, task.labels.all())

    def test_label_can_be_used_in_multiple_tasks(self):
        """Проверяет, что метка может использоваться в нескольких задачах"""
        task1 = Task.objects.create(
            name='Задача 1',
            status=self.status,
            author=self.user
        )
        task2 = Task.objects.create(
            name='Задача 2',
            status=self.status,
            author=self.user
        )

        task1.labels.add(self.bug_label)
        task2.labels.add(self.bug_label)

        self.assertEqual(self.bug_label.tasks.count(), 2)
        self.assertIn(task1, self.bug_label.tasks.all())
        self.assertIn(task2, self.bug_label.tasks.all())

    def test_task_without_labels(self):
        """Проверяет, что задача может быть создана без меток"""
        task = Task.objects.create(
            name='Задача без меток',
            status=self.status,
            author=self.user
        )
        self.assertEqual(task.labels.count(), 0)

    def test_label_related_name(self):
        """Проверяет, что related_name работает корректно"""
        task = Task.objects.create(
            name='Тестовая задача',
            status=self.status,
            author=self.user
        )
        task.labels.add(self.bug_label)

        # Проверяем доступ через related_name
        self.assertEqual(self.bug_label.tasks.count(), 1)
        self.assertEqual(self.bug_label.tasks.first(), task)

    def test_remove_label_from_task(self):
        """Проверяет удаление метки из задачи"""
        task = Task.objects.create(
            name='Тестовая задача',
            status=self.status,
            author=self.user
        )
        task.labels.add(self.bug_label, self.feature_label)

        task.labels.remove(self.bug_label)

        self.assertEqual(task.labels.count(), 1)
        self.assertNotIn(self.bug_label, task.labels.all())
        self.assertIn(self.feature_label, task.labels.all())