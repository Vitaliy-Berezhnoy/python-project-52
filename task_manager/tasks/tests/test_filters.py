from django.contrib.auth import get_user_model
from django.test import TestCase
from django_filters import FilterSet

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task

User = get_user_model()
TEST_PASSWORD = "ValidPassword123!"


class TaskFilterTest(TestCase):
    """Тесты для фильтрации задач"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.author = User.objects.create_user(
            username="author",
            password=TEST_PASSWORD,
            first_name="Автор",
            last_name="Тестов",
        )
        self.executor = User.objects.create_user(
            username="executor",
            password=TEST_PASSWORD,
            first_name="Исполнитель",
            last_name="Тестов",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password=TEST_PASSWORD,
            first_name="Другой",
            last_name="Пользователь",
        )

        # Создаем статусы
        self.status_new = Status.objects.create(name="новый")
        self.status_in_progress = Status.objects.create(name="в работе")
        self.status_completed = Status.objects.create(name="завершен")

        # Создаем метки
        self.label_work = Label.objects.create(name="Работа")
        self.label_personal = Label.objects.create(name="Личное")

        # Создаем тестовые задачи
        self.task1 = Task.objects.create(
            name="Первая задача автора",
            description="Описание первой задачи",
            status=self.status_new,
            author=self.author,
            executor=self.executor,
        )
        self.task1.labels.add(self.label_work)

        self.task2 = Task.objects.create(
            name="Вторая задача автора",
            description="Описание второй задачи",
            status=self.status_in_progress,
            author=self.author,
            executor=self.other_user,
        )
        self.task2.labels.add(self.label_personal)

        self.task3 = Task.objects.create(
            name="Задача другого пользователя",
            description="Описание задачи другого пользователя",
            status=self.status_completed,
            author=self.other_user,
            executor=self.author,
        )
        self.task3.labels.add(self.label_work, self.label_personal)

    def test_task_filter_creation(self):
        """Проверяет, что фильтр создается корректно"""

        # Создаем mock request с пользователем
        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        # Создаем фильтр с mock request
        task_filter = TaskFilter(
            data={}, queryset=Task.objects.all(), request=mock_request
        )

        self.assertIsInstance(task_filter, FilterSet)
        self.assertIn("status", task_filter.filters)
        self.assertIn("executor", task_filter.filters)
        self.assertIn("labels", task_filter.filters)
        self.assertIn("self_tasks", task_filter.filters)

    def test_filter_by_status(self):
        """Проверяет фильтрацию по статусу"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        # Фильтруем по статусу "новый"
        task_filter = TaskFilter(
            data={"status": self.status_new.id},
            queryset=Task.objects.all(),
            request=mock_request,
        )

        filtered_tasks = task_filter.qs
        self.assertEqual(filtered_tasks.count(), 1)
        self.assertEqual(filtered_tasks.first(), self.task1)

    def test_filter_by_executor(self):
        """Проверяет фильтрацию по исполнителю"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        # Фильтруем по исполнителю
        task_filter = TaskFilter(
            data={"executor": self.executor.id},
            queryset=Task.objects.all(),
            request=mock_request,
        )

        filtered_tasks = task_filter.qs
        self.assertEqual(filtered_tasks.count(), 1)
        self.assertEqual(filtered_tasks.first(), self.task1)

    def test_filter_by_labels(self):
        """Проверяет фильтрацию по меткам"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        # Фильтруем по метке "Работа"
        task_filter = TaskFilter(
            data={"labels": self.label_work.id},
            queryset=Task.objects.all(),
            request=mock_request,
        )

        filtered_tasks = task_filter.qs
        self.assertEqual(filtered_tasks.count(), 2)  # task1 и task3
        self.assertIn(self.task1, filtered_tasks)
        self.assertIn(self.task3, filtered_tasks)

    def test_filter_self_tasks_true(self):
        """Проверяет фильтрацию 'только мои задачи' (True)"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        # Фильтруем только задачи автора
        task_filter = TaskFilter(
            data={"self_tasks": True},
            queryset=Task.objects.all(),
            request=mock_request,
        )

        filtered_tasks = task_filter.qs
        self.assertEqual(filtered_tasks.count(), 2)  # task1 и task2
        self.assertIn(self.task1, filtered_tasks)
        self.assertIn(self.task2, filtered_tasks)
        self.assertNotIn(self.task3, filtered_tasks)

    def test_filter_self_tasks_false(self):
        """Проверяет фильтрацию 'только мои задачи' (False)"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        # Не фильтруем по автору (показываем все задачи)
        task_filter = TaskFilter(
            data={"self_tasks": False},
            queryset=Task.objects.all(),
            request=mock_request,
        )

        filtered_tasks = task_filter.qs
        self.assertEqual(filtered_tasks.count(), 3)  # все задачи
        self.assertIn(self.task1, filtered_tasks)
        self.assertIn(self.task2, filtered_tasks)
        self.assertIn(self.task3, filtered_tasks)

    def test_filter_self_tasks_no_value(self):
        """Проверяет фильтрацию когда 'только мои задачи' не указано"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        # Не указываем фильтр self_tasks
        task_filter = TaskFilter(
            data={}, queryset=Task.objects.all(), request=mock_request
        )

        filtered_tasks = task_filter.qs
        self.assertEqual(filtered_tasks.count(), 3)  # все задачи
        self.assertIn(self.task1, filtered_tasks)
        self.assertIn(self.task2, filtered_tasks)
        self.assertIn(self.task3, filtered_tasks)

    def test_filter_combined(self):
        """Проверяет комбинированную фильтрацию"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        # Фильтруем по статусу и метке одновременно
        task_filter = TaskFilter(
            data={"status": self.status_new.id, "labels": self.label_work.id},
            queryset=Task.objects.all(),
            request=mock_request,
        )

        filtered_tasks = task_filter.qs
        self.assertEqual(filtered_tasks.count(), 1)
        self.assertEqual(filtered_tasks.first(), self.task1)

    def test_filter_ordering(self):
        """Проверяет, что queryset упорядочен правильно"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        task_filter = TaskFilter(
            data={}, queryset=Task.objects.all(), request=mock_request
        )

        filtered_tasks = task_filter.qs
        # Проверяем порядок по убыванию created_at (новые задачи первыми)
        self.assertEqual(filtered_tasks[0], self.task3)  # Самая новая
        self.assertEqual(filtered_tasks[1], self.task2)
        self.assertEqual(filtered_tasks[2], self.task1)  # Самая старая

    def test_empty_label_queryset_ordering(self):
        """Проверяет упорядочивание меток по имени"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        task_filter = TaskFilter(
            data={}, queryset=Task.objects.all(), request=mock_request
        )

        # Проверяем, что метки упорядочены по имени
        labels_queryset = task_filter.filters["labels"].queryset
        labels_names = list(labels_queryset.values_list("name", flat=True))
        self.assertEqual(
            labels_names, ["Личное", "Работа"]
        )  # В алфавитном порядке

    def test_empty_status_queryset_ordering(self):
        """Проверяет упорядочивание статусов по имени"""

        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.author)

        task_filter = TaskFilter(
            data={}, queryset=Task.objects.all(), request=mock_request
        )

        # Проверяем, что статусы упорядочены по имени
        status_queryset = task_filter.filters["status"].queryset
        status_names = list(status_queryset.values_list("name", flat=True))
        self.assertEqual(
            status_names, ["в работе", "завершен", "новый"]
        )  # В алфавитном порядке
