from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()
TEST_PASSWORD = "ValidPassword123!"


class TasksViewsTest(TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.client = Client()
        self.author = User.objects.create_user(
            username="author",
            password=TEST_PASSWORD,
            first_name="Автор",
            last_name="Задач",
        )
        self.executor = User.objects.create_user(
            username="executor",
            password=TEST_PASSWORD,
            first_name="Исполнитель",
            last_name="Задач",
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password=TEST_PASSWORD
        )
        self.status = Status.objects.create(name="новый")
        self.task = Task.objects.create(
            name="Тестовая задача",
            description="Описание тестовой задачи",
            status=self.status,
            author=self.author,
            executor=self.executor,
        )

    def test_tasks_list_view_requires_login(self):
        """Проверяет, что доступ к списку задач требует авторизации"""
        response = self.client.get(reverse("tasks:tasks"))
        self.assertEqual(response.status_code, 302)  # Редирект на логин

    def test_tasks_list_view_authenticated(self):
        """Проверяет, что авторизованный пользователь может видеть список задач"""
        self.client.login(username="author", password=TEST_PASSWORD)
        response = self.client.get(reverse("tasks:tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertContains(response, "Тестовая задача")

    def test_task_create_view_requires_login(self):
        """Проверяет, что доступ к форме создания задачи требует авторизации"""
        response = self.client.get(reverse("tasks:create"))
        self.assertEqual(response.status_code, 302)

    def test_task_create_view_authenticated(self):
        """Проверяет, что авторизованный пользователь может получить форму создания задачи"""
        self.client.login(username="author", password=TEST_PASSWORD)
        response = self.client.get(reverse("tasks:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/create.html")

    def test_task_create_post_authenticated(self):
        """Проверяет создание задачи с валидными данными"""
        self.client.login(username="author", password=TEST_PASSWORD)
        form_data = {
            "name": "Новая задача",
            "description": "Описание новой задачи",
            "status": self.status.id,
            "executor": self.executor.id,
        }

        task_count_before = Task.objects.count()
        response = self.client.post(reverse("tasks:create"), data=form_data)

        self.assertEqual(response.status_code, 302)  # Редирект после успеха
        self.assertRedirects(response, reverse("tasks:tasks"))
        self.assertEqual(Task.objects.count(), task_count_before + 1)

        # Проверяем, что автор установлен автоматически
        new_task = Task.objects.get(name="Новая задача")
        self.assertEqual(new_task.author, self.author)

    def test_task_detail_view_requires_login(self):
        """Проверяет, что доступ к детальной странице задачи требует авторизации"""
        response = self.client.get(reverse("tasks:detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

    def test_task_detail_view_authenticated(self):
        """Проверяет, что авторизованный пользователь может просматривать задачу"""
        self.client.login(username="author", password=TEST_PASSWORD)
        response = self.client.get(reverse("tasks:detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/detail.html")
        self.assertContains(response, "Тестовая задача")

    def test_task_update_view_requires_login(self):
        """Проверяет, что доступ к форме редактирования задачи требует авторизации"""
        response = self.client.get(reverse("tasks:update", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

    def test_task_update_view_authenticated(self):
        """Проверяет, что авторизованный пользователь может редактировать задачу"""
        self.client.login(username="author", password=TEST_PASSWORD)
        response = self.client.get(reverse("tasks:update", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/update.html")

    def test_task_update_post_authenticated(self):
        """Проверяет обновление задачи с валидными данными"""
        self.client.login(username="author", password=TEST_PASSWORD)
        form_data = {
            "name": "Обновленная задача",
            "description": "Обновленное описание",
            "status": self.status.id,
            "executor": self.executor.id,
        }

        response = self.client.post(
            reverse("tasks:update", args=[self.task.id]), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:tasks"))

        # Проверяем, что задача была обновлена
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Обновленная задача")
        self.assertEqual(self.task.description, "Обновленное описание")

    def test_task_delete_view_requires_login(self):
        """Проверяет, что доступ к форме удаления задачи требует авторизации"""
        response = self.client.get(reverse("tasks:delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

    def test_task_delete_view_authenticated_author(self):
        """Проверяет, что автор задачи может получить форму удаления"""
        self.client.login(username="author", password=TEST_PASSWORD)
        response = self.client.get(reverse("tasks:delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/delete.html")

    def test_task_delete_view_authenticated_non_author(self):
        """Проверяет, что не-автор НЕ может получить форму удаления"""
        self.client.login(username="otheruser", password=TEST_PASSWORD)
        response = self.client.get(reverse("tasks:delete", args=[self.task.id]))
        self.assertEqual(
            response.status_code, 302
        )  # Редирект с сообщением об ошибке
        self.assertRedirects(response, reverse("tasks:tasks"))

    def test_task_delete_post_authenticated_author(self):
        """Проверяет, что автор может удалить задачу"""
        self.client.login(username="author", password=TEST_PASSWORD)

        task_count_before = Task.objects.count()
        response = self.client.post(
            reverse("tasks:delete", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:tasks"))
        self.assertEqual(Task.objects.count(), task_count_before - 1)

    def test_task_delete_post_authenticated_non_author(self):
        """Проверяет, что не-автор НЕ может удалить задачу"""
        self.client.login(username="otheruser", password=TEST_PASSWORD)

        task_count_before = Task.objects.count()
        response = self.client.post(
            reverse("tasks:delete", args=[self.task.id])
        )

        # Должен быть редирект с сообщением об ошибке
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:tasks"))
        # Задача не должна быть удалена
        self.assertEqual(Task.objects.count(), task_count_before)


class TaskPermissionTest(TestCase):
    """Тесты для проверки прав доступа к задачам"""

    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username="author", password=TEST_PASSWORD
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password=TEST_PASSWORD
        )
        self.status = Status.objects.create(name="новый")
        self.task = Task.objects.create(
            name="Тестовая задача", status=self.status, author=self.author
        )

    def test_only_author_can_delete_task(self):
        """Проверяет, что только автор может удалить задачу"""
        # Автор может удалить
        self.client.login(username="author", password=TEST_PASSWORD)
        response = self.client.post(
            reverse("tasks:delete", args=[self.task.id])
        )
        self.assertEqual(response.status_code, 302)

        # Создаем новую задачу для следующего теста
        task2 = Task.objects.create(
            name="Другая задача", status=self.status, author=self.author
        )

        # Не-автор не может удалить
        self.client.login(username="otheruser", password=TEST_PASSWORD)
        task_count_before = Task.objects.count()
        response = self.client.post(reverse("tasks:delete", args=[task2.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Task.objects.count(), task_count_before
        )  # Задача не удалена
