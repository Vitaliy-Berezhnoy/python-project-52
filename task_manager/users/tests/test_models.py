from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "композитор",
            "password": "password123",
            "first_name": "Арам",
            "last_name": "Хачатурян",
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, "композитор")
        self.assertEqual(user.first_name, "Арам")
        self.assertEqual(user.last_name, "Хачатурян")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username="admin", password="admin_password123"
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_string_representation(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), "композитор")

    def test_user_verbose_names(self):
        self.assertEqual(User._meta.verbose_name, _("User"))
        self.assertEqual(User._meta.verbose_name_plural, _("Users"))

    def test_user_table_name(self):
        self.assertEqual(User._meta.db_table, "users")

    def test_user_has_created_at_and_updated_at(self):
        user = User.objects.create_user(**self.user_data)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
