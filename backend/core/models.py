"""
Database models
"""
import uuid
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone


def student_image_file_path(instance, filename):
    """Generate file path for new student image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email='test@example.com', password='test', **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create, save and return a new superuser"""
        if not email:
            raise ValueError('Superuser must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Course(models.Model):
    """Course object"""
    class StatusType(models.IntegerChoices):
        """Transaction choices"""
        ACTIVE = 1
        INACTIVE = 2

    name = models.CharField(max_length=255)
    status = models.SmallIntegerField(choices=StatusType.choices)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.name


class Student(models.Model):
    """Student object"""
    name = models.CharField(max_length=255)
    photo = models.ImageField(null=True, upload_to=student_image_file_path)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name
