from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()
TEST_PASSWORD = 'ValidPassword123!'


class StatusesViewsTest(TestCase):
    def setUp(self):
        """Подготовка тестовых данных - создаем пользователя и тестовый статус"""
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='testuser',
            password=TEST_PASSWORD
        )
        self.status = Status.objects.create(name='новый')

    def test_statuses_list_view_authenticated(self):
        """Проверяет, что авторизованный пользователь может видеть список статусов"""
        self.client.login(username='testuser', password=TEST_PASSWORD)
        response = self.client.get(reverse('statuses:statuses'))
        self.assertEqual(response.status_code, 200)  # Успешный доступ
        self.assertTemplateUsed(response, 'statuses/index.html')  # Используется правильный шаблон
        self.assertContains(response, 'новый')  # Статус отображается на странице

    def test_status_create_view_authenticated(self):
        """Проверяет, что авторизованный пользователь может получить форму создания статуса"""
        self.client.login(username='testuser', password=TEST_PASSWORD)
        response = self.client.get(reverse('statuses:create'))
        self.assertEqual(response.status_code, 200)  # Успешный доступ к форме
        self.assertContains(response, 'name="name"')  # Поле name существует
        self.assertContains(response, _('Name'))  # Правильная метка поля
        self.assertTemplateUsed(response, 'statuses/create.html')  # Используется правильный шаблон

    def test_status_create_post_authenticated(self):
        """Проверяет, что авторизованный пользователь может создать статус через POST-запрос"""
        self.client.login(username='testuser', password=TEST_PASSWORD)
        form_data = {'name': 'в работе'}

        # Проверяем количество статусов до создания
        status_count_before = Status.objects.count()

        response = self.client.post(reverse('statuses:create'), data=form_data)

        # Проверяем редирект после успешного создания
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:statuses'))

        # Проверяем, что статус был создан
        self.assertEqual(Status.objects.count(), status_count_before + 1)
        self.assertTrue(Status.objects.filter(name='в работе').exists())

    def test_status_create_with_invalid_data(self):
        """Проверяет, что форма не принимает невалидные данные"""
        self.client.login(username='testuser', password=TEST_PASSWORD)
        form_data = {'name': ''}  # Пустое имя

        response = self.client.post(reverse('statuses:create'), data=form_data)

        self.assertEqual(response.status_code, 200)  # Остается на странице
#        self.assertContains(response, 'This field is required')  # Сообщение об ошибке

    def test_status_update_view_authenticated(self):
        """Проверяет, что авторизованный пользователь может получить форму редактирования статуса"""
        self.client.login(username='testuser', password=TEST_PASSWORD)
        response = self.client.get(reverse('statuses:update', args=[self.status.id]))
        self.assertEqual(response.status_code, 200)  # Успешный доступ к форме
        self.assertTemplateUsed(response, 'statuses/update.html')  # Используется правильный шаблон
        self.assertContains(response, self.status.name)  # Форма содержит текущее имя статуса

    def test_status_update_post_authenticated(self):
        """Проверяет, что авторизованный пользователь может обновить статус через POST-запрос"""
        self.client.login(username='testuser', password=TEST_PASSWORD)
        form_data = {'name': 'обновленный статус'}

        response = self.client.post(reverse('statuses:update', args=[self.status.id]), data=form_data)

        # Проверяем редирект после успешного обновления
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:statuses'))

        # Проверяем, что статус был обновлен
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'обновленный статус')

    def test_status_update_with_invalid_data(self):
        """Проверяет, что форма редактирования не принимает невалидные данные"""
        self.client.login(username='testuser', password=TEST_PASSWORD)
        form_data = {'name': ''}  # Пустое имя

        response = self.client.post(
            reverse('statuses:update', args=[self.status.id]),
            data=form_data
        )

        self.assertEqual(response.status_code, 200)  # Остается на странице
#        self.assertContains(response, 'This field is required')  # Сообщение об ошибке

    def test_status_delete_view_authenticated(self):
        """Проверяет, что авторизованный пользователь может получить форму удаления статуса"""
        self.client.login(username='testuser', password=TEST_PASSWORD)
        response = self.client.get(reverse('statuses:delete', args=[self.status.id]))
        self.assertEqual(response.status_code, 200)  # Успешный доступ к форме
        self.assertTemplateUsed(response, 'statuses/delete.html')  # Используется правильный шаблон
        self.assertContains(response, self.status.name)  # Форма содержит имя статуса для подтверждения

    def test_status_delete_post_authenticated(self):
        """Проверяет, что авторизованный пользователь может удалить статус через POST-запрос"""
        self.client.login(username='testuser', password=TEST_PASSWORD)

        # Проверяем количество статусов до удаления
        status_count_before = Status.objects.count()

        response = self.client.post(reverse('statuses:delete', args=[self.status.id]))

        # Проверяем редирект после успешного удаления
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:statuses'))

        # Проверяем, что статус был удален
        self.assertEqual(Status.objects.count(), status_count_before - 1)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_statuses_list_shows_all_statuses(self):
        """Проверяет, что на странице списка отображаются все созданные статусы"""
        self.client.login(username='testuser', password=TEST_PASSWORD)

        # Создаем дополнительные статусы
        Status.objects.create(name='в работе')
        Status.objects.create(name='завершен')

        response = self.client.get(reverse('statuses:statuses'))

        # Проверяем, что все статусы отображаются
        self.assertContains(response, 'новый')
        self.assertContains(response, 'в работе')
        self.assertContains(response, 'завершен')

    def test_statuses_list_ordered_correctly(self):
        """Проверяет, что статусы отображаются в правильном порядке (по ID)"""
        self.client.login(username='testuser', password=TEST_PASSWORD)

        # Создаем статусы в разном порядке
        Status.objects.create(name='первый')
        Status.objects.create(name='второй')
        Status.objects.create(name='третий')

        response = self.client.get(reverse('statuses:statuses'))

        # Проверяем порядок отображения (должен быть по возрастанию ID)
        content = response.content.decode()
        pos1 = content.find('первый')
        pos2 = content.find('второй')
        pos3 = content.find('третий')

        # Статусы должны идти в порядке их ID (pos1 < pos2 < pos3)
        self.assertLess(pos1, pos2)
        self.assertLess(pos2, pos3)