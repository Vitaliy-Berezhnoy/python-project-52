from django.test import TestCase

from task_manager.users.forms import UserRegistrationForm
from task_manager.users.models import User


class UserRegistrationFormTest(TestCase):
    def test_valid_registration_form(self):
        form_data = {
            "username": "революционер",
            "first_name": "Анастас",
            "last_name": "Микоян",
            "password1": "t3!",    # NOSONAR
            "password2": "t3!",    # NOSONAR
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_too_short(self):
        form_data = {
            "username": "революционер",
            "first_name": "Анастас",
            "last_name": "Микоян",
            "password1": "12",    # NOSONAR
            "password2": "12",    # NOSONAR
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_passwords_do_not_match(self):
        form_data = {
            "username": "революционер",
            "first_name": "Анастас",
            "last_name": "Микоян",
            "password1": "password123",    # NOSONAR
            "password2": "different",    # NOSONAR
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_username_already_exists(self):
        User.objects.create_user(username="актер", password="password123")
        form_data = {
            "username": "актер",
            "first_name": "Фрунзик",
            "last_name": "Мкртчян",
            "password1": "password123",    # NOSONAR
            "password2": "password123",    # NOSONAR
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class UserUpdateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            first_name="Old",
            last_name="Name",
        )

    def test_valid_update(self):
        form_data = {
            "username": "updateduser",
            "first_name": "Updated",
            "last_name": "Name",
        }
        form = UserRegistrationForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_has_no_password_field(self):
        form = UserRegistrationForm(instance=self.user)
        self.assertNotIn("password", form.fields)

    def test_update_saves_correctly(self):
        form_data = {
            "username": "updateduser",
            "first_name": "Updated",
            "last_name": "Name",
        }
        form = UserRegistrationForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.first_name, "Updated")
