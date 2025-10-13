from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

UserModel = get_user_model()

TEST_PASSWORD = "ValidPassword123!"


class UsersViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username="testuser",
            password=TEST_PASSWORD,
            first_name="Test",
            last_name="User",
        )
        self.other_user = UserModel.objects.create_user(
            username="otheruser",
            password="otherpass123!",
            first_name="Other",
            last_name="User",
        )

    def test_users_list_view(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/index.html")
        self.assertContains(response, "testuser")
        self.assertContains(response, "otheruser")

    def test_user_create_view_get(self):
        response = self.client.get(reverse("user_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/new_user.html")

    def test_user_create_view_post(self):
        form_data = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "password1": TEST_PASSWORD,
            "password2": TEST_PASSWORD,
        }
        response = self.client.post(reverse("user_create"), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(UserModel.objects.filter(username="newuser").exists())

    def test_user_update_view_requires_login(self):
        response = self.client.get(reverse("user_update", args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_user_update_view_own_profile(self):
        self.client.login(username="testuser", password=TEST_PASSWORD)
        response = self.client.get(reverse("user_update", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/update.html")

    def test_user_update_view_other_profile(self):
        self.client.login(username="testuser", password=TEST_PASSWORD)
        response = self.client.get(
            reverse("user_update", args=[self.other_user.id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to users list
        self.assertRedirects(response, reverse("users"))

    def test_user_delete_view(self):
        self.client.login(username="testuser", password=TEST_PASSWORD)
        response = self.client.get(reverse("user_delete", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/delete.html")

    def test_user_delete_view_other_user(self):
        self.client.login(username="testuser", password=TEST_PASSWORD)
        response = self.client.get(
            reverse("user_delete", args=[self.other_user.id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to users list
        self.assertRedirects(response, reverse("users"))


class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username="testuser", password=TEST_PASSWORD
        )

    def test_login_view_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_view_post_valid(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": TEST_PASSWORD},
        )
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_login_view_post_invalid(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)  # Stays on login page
        self.assertContains(
            response, "Please enter correct username and password"
        )

    def test_logout_view_requires_login(self):
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_logout_view(self):
        self.client.login(username="testuser", password=TEST_PASSWORD)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirect after logout


def test_authenticated_user_can_access_their_profile(self):
    """пользователь может редактировать свой профиль"""
    self.client.login(username="testuser", password="password123!")
    response = self.client.get(reverse("user_update", args=[self.user.id]))
    self.assertEqual(response.status_code, 200)


def test_anonymous_user_cannot_delete_users(self):
    """аноним не может удалять пользователей"""
    response = self.client.get(reverse("user_delete", args=[1]))
    self.assertNotEqual(response.status_code, 200)  # Не должен иметь доступ
