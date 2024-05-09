from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Student
from attendance.logic import FaceRecognitionUseCase

import face_recognition
import json

from rest_framework.exceptions import ValidationError


def save_student_encodings(student: Student):
    face = face_recognition.load_image_file(student.photo.path)
    face_bounding_boxes = face_recognition.face_locations(face)

    if len(face_bounding_boxes) == 1:
        student.face_encoding = face_recognition.face_encodings(face)[0].tolist()
        student.save(update_fields=["face_encoding"])
    else:
        student.delete()
        raise ValidationError("The provided photo has more than one face")


@receiver(post_save, sender=Student)
def student_created(sender, instance, created, **kwargs):
    if created:
        save_student_encodings(instance)

    FaceRecognitionUseCase.train()
