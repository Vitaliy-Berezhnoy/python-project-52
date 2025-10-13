from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()
TEST_PASSWORD = "ValidPassword123!"


class LabelsViewsTest(TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password=TEST_PASSWORD
        )
        self.label = Label.objects.create(name="bug")

    def test_labels_list_view_requires_login(self):
        """доступ к списку меток требует авторизации"""
        response = self.client.get(reverse("labels:labels"))
        self.assertEqual(response.status_code, 302)  # Редирект на логин

    def test_labels_list_view_authenticated(self):
        """авторизованный пользователь может видеть список меток"""
        self.client.login(username="testuser", password=TEST_PASSWORD)
        response = self.client.get(reverse("labels:labels"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/index.html")
        self.assertContains(response, "bug")

    def test_label_create_view_requires_login(self):
        """доступ к форме создания метки требует авторизации"""
        response = self.client.get(reverse("labels:create"))
        self.assertEqual(response.status_code, 302)

    def test_label_create_view_authenticated(self):
        """авторизованный пользователь может получить форму создания метки"""
        self.client.login(username="testuser", password=TEST_PASSWORD)
        response = self.client.get(reverse("labels:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/create.html")

    def test_label_create_post_authenticated(self):
        """Проверяет создание метки с валидными данными"""
        self.client.login(username="testuser", password=TEST_PASSWORD)
        form_data = {"name": "feature"}

        label_count_before = Label.objects.count()
        response = self.client.post(reverse("labels:create"), data=form_data)

        self.assertEqual(response.status_code, 302)  # Редирект после успеха
        self.assertRedirects(response, reverse("labels:labels"))
        self.assertEqual(Label.objects.count(), label_count_before + 1)
        self.assertTrue(Label.objects.filter(name="feature").exists())

    def test_label_update_view_requires_login(self):
        """доступ к форме редактирования метки требует авторизации"""
        response = self.client.get(
            reverse("labels:update", args=[self.label.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_label_update_view_authenticated(self):
        """авторизованный пользователь может редактировать метку"""
        self.client.login(username="testuser", password=TEST_PASSWORD)
        response = self.client.get(
            reverse("labels:update", args=[self.label.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/update.html")

    def test_label_update_post_authenticated(self):
        """Проверяет обновление метки с валидными данными"""
        self.client.login(username="testuser", password=TEST_PASSWORD)
        form_data = {"name": "critical bug"}

        response = self.client.post(
            reverse("labels:update", args=[self.label.id]), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels:labels"))

        # Проверяем, что метка была обновлена
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "critical bug")

    def test_label_delete_view_requires_login(self):
        """доступ к форме удаления метки требует авторизации"""
        response = self.client.get(
            reverse("labels:delete", args=[self.label.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_label_delete_view_authenticated(self):
        """авторизованный пользователь может получить форму удаления метки"""
        self.client.login(username="testuser", password=TEST_PASSWORD)
        response = self.client.get(
            reverse("labels:delete", args=[self.label.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/delete.html")

    def test_label_delete_post_authenticated(self):
        """Проверяет удаление метки без связанных задач"""
        self.client.login(username="testuser", password=TEST_PASSWORD)

        label_count_before = Label.objects.count()
        response = self.client.post(
            reverse("labels:delete", args=[self.label.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels:labels"))
        self.assertEqual(Label.objects.count(), label_count_before - 1)


class LabelDeleteProtectionTest(TestCase):
    """Тесты для защиты от удаления используемых меток"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password=TEST_PASSWORD
        )
        self.status = Status.objects.create(name="новый")
        self.label = Label.objects.create(name="bug")

        # Создаем задачу с меткой
        self.task = Task.objects.create(
            name="Тестовая задача", status=self.status, author=self.user
        )
        self.task.labels.add(self.label)

    def test_cannot_delete_label_with_tasks(self):
        """метка с связанными задачами не может быть удалена"""
        self.client.login(username="testuser", password=TEST_PASSWORD)

        label_count_before = Label.objects.count()
        response = self.client.post(
            reverse("labels:delete", args=[self.label.id])
        )

        # Должен быть редирект с сообщением об ошибке
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels:labels"))
        # Метка не должна быть удалена
        self.assertEqual(Label.objects.count(), label_count_before)

    def test_can_delete_label_without_tasks(self):
        """метка без связанных задач может быть удалена"""
        # Удаляем связь с задачей
        self.task.labels.remove(self.label)

        self.client.login(username="testuser", password=TEST_PASSWORD)

        label_count_before = Label.objects.count()
        response = self.client.post(
            reverse("labels:delete", args=[self.label.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), label_count_before - 1)
