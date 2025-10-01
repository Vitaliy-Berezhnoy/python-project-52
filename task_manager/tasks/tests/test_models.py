from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status

User = get_user_model()
TEST_PASSWORD = 'ValidPassword123!'


class TaskModelTest(TestCase):
    def setUp(self):
        """Подготовка тестовых данных - создаем пользователей, статус и задачу"""
        self.user = User.objects.create_user(
            username='author',
            password=TEST_PASSWORD
        )
        self.executor = User.objects.create_user(
            username='executor',
            password=TEST_PASSWORD
        )
        self.status = Status.objects.create(name='новый')
        self.task_data = {
            'name': 'Тестовая задача',
            'description': 'Описание тестовой задачи',
            'status': self.status,
            'author': self.user,
            'executor': self.executor,
        }

    def test_create_task(self):
        """Проверяет, что задача создается с правильными атрибутами"""
        task = Task.objects.create(**self.task_data)
        self.assertEqual(task.name, 'Тестовая задача')
        self.assertEqual(task.description, 'Описание тестовой задачи')
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.author, self.user)
        self.assertEqual(task.executor, self.executor)
        self.assertIsNotNone(task.created_at)

    def test_task_string_representation(self):
        """Проверяет, что строковое представление задачи возвращает её имя"""
        task = Task.objects.create(**self.task_data)
        self.assertEqual(str(task), 'Тестовая задача')

    def test_task_verbose_names(self):
        """Проверяет, что verbose_name и verbose_name_plural настроены правильно"""
        self.assertEqual(Task._meta.verbose_name, _('Task'))
        self.assertEqual(Task._meta.verbose_name_plural, _('Tasks'))

    def test_task_table_name(self):
        """Проверяет, что имя таблицы в базе данных установлено правильно"""
        self.assertEqual(Task._meta.db_table, 'tasks')

    def test_task_ordering(self):
        """Проверяет порядок задач по умолчанию (по убыванию даты создания)"""
        task1 = Task.objects.create(
            name='Первая задача',
            status=self.status,
            author=self.user
        )
        task2 = Task.objects.create(
            name='Вторая задача',
            status=self.status,
            author=self.user
        )

        all_tasks = Task.objects.all()
        self.assertEqual(all_tasks[0], task2)  # Новые задачи первыми
        self.assertEqual(all_tasks[1], task1)

    def test_task_without_executor(self):
        """Проверяет, что задача может быть создана без исполнителя"""
        task = Task.objects.create(
            name='Задача без исполнителя',
            status=self.status,
            author=self.user,
            executor=None
        )
        self.assertIsNone(task.executor)

    def test_task_required_fields(self):
        """Проверяет, что обязательные поля действительно обязательны"""
        with self.assertRaises(Exception):
            Task.objects.create()  # Без обязательных полей

    def test_task_foreign_key_relationships(self):
        """Проверяет связи с другими моделями через ForeignKey"""
        task = Task.objects.create(**self.task_data)

        # Проверяем связь со статусом
        self.assertEqual(task.status.name, 'новый')

        # Проверяем связь с автором
        self.assertEqual(task.author.username, 'author')

        # Проверяем связь с исполнителем
        self.assertEqual(task.executor.username, 'executor')

    def test_task_author_protected_deletion(self):
        """Проверяет, что автор не может быть удален если у него есть задачи"""
        Task.objects.create(**self.task_data)

        # Попытка удалить автора должна вызвать ProtectedError
        with self.assertRaises(Exception):
            self.user.delete()

    def test_task_status_protected_deletion(self):
        """Проверяет, что статус не может быть удален если используется в задачах"""
        Task.objects.create(**self.task_data)

        # Попытка удалить статус должна вызвать ProtectedError
        with self.assertRaises(Exception):
            self.status.delete()