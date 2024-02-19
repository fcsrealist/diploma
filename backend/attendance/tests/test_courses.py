"""
Tests for the courses api
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import (
    Course,
    Student
)

ATTENDANCE_URL = reverse('attendance:course-list')


def detail_url(course_id):
    """Create and return a course detail URL"""
    return reverse('attendance:course-detail', args=[course_id])


def create_course(user, **params):
    """Create course instance"""
    defaults = {
        'name': 'Sample course name',
        'status': Course.StatusType.ACTIVE
    }
    defaults.update(params)

    course = Course.objects.create(user=user, **defaults)
    return course


def create_student(name='Sample student name'):
    """Create student instance"""
    return Student.objects.create(name=name)


class PrivateCoursesAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user()
        self.client.force_authenticate(self.user)

    def test_create_course(self):
        """Test create course"""
        payload = {
            'name': 'Sample course name',
            'status': Course.StatusType.ACTIVE,
            'student_ids': [create_student().id]
        }
        res = self.client.post(ATTENDANCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        course = Course.objects.get(id=res.data['id'])

        for k, v in payload.items():
            if k != 'student_ids':
                self.assertEqual(getattr(course, k), v)
        self.assertEqual(course.user, self.user)
        self.assertEqual(course.students.count(), 1)

    def test_update_course(self):
        """Test update course"""
        course = create_course(self.user)
        payload = {
            'name': 'Sample course name',
            'status': Course.StatusType.ACTIVE,
            'student_ids': [create_student().id, create_student().id]
        }
        url = detail_url(course.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        for k, v in payload.items():
            if k != 'student_ids':
                self.assertEqual(getattr(course, k), v)
        self.assertEqual(course.user, self.user)
        self.assertEqual(course.students.count(), 2)

    def test_delete_recipe(self):
        """Test delete course."""
        course = create_course(user=self.user)

        url = detail_url(course.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=course.id).exists())
