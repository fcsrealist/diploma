"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelsTests(TestCase):
    """Test models"""

    def test_create_user_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@exapmle.com"
        password = "1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEquals(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEquals(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test132')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_course(self):
        """Test creating a course"""
        user = get_user_model().objects.create_user()

        course = models.Course.objects.create(
            user=user,
            name='Sample course name',
            status=models.Course.StatusType.ACTIVE
        )

        self.assertEqual(str(course), course.name)

    def test_create_student(self):
        """Test creating a course"""
        student = models.Student.objects.create(
            name='Sample student name'
        )

        self.assertEqual(str(student), student.name)
