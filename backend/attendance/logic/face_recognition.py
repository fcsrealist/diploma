from core.models import Course
from django.core.files.storage import FileSystemStorage
from rest_framework.exceptions import APIException

from core.models import Student, Attendance

import face_recognition
import pickle
import os


class FaceRecognitionUseCase:
    def __init__(self, course: Course, image):
        self.course = course
        self.image_name = self._get_image_name(image)

    def execute(self) -> None:
        students = self._get_attended_students()
        course_students = self.course.students.all()
        for student in course_students:
            if student.name in students:
                Attendance.objects.create(
                    course=self.course,
                    student=student,
                    status=Attendance.StatusType.ATTENDED
                )
            else:
                Attendance.objects.create(
                    course=self.course,
                    student=student,
                    status=Attendance.StatusType.ABSENT
                )

    def _get_attended_students(self, threshold=0.5) -> list:
        try:
            test_image = face_recognition.load_image_file('attendance/logic/files/' + self.image_name)
            face_locations = face_recognition.face_locations(test_image)
            face_encodings = (face_recognition
                              .face_encodings(test_image, face_locations))

            predictions = []

            clf = pickle.load(open('attendance/logic/files/trained_model.pickle', 'rb'))

            for x in face_encodings:
                closest = clf.kneighbors([x], n_neighbors=1)
                if closest[0][0][0] <= threshold:
                    predictions.append(clf.predict([x])[0])
                else:
                    predictions.append('')
        except Exception:
            os.remove('attendance/logic/files/' + self.image_name)
            raise APIException("Произошла ошибка запроса", code="400;")
        os.remove('attendance/logic/files/' + self.image_name)

        return predictions

    def _get_image_name(self, image):
        fs = FileSystemStorage(location='attendance/logic/files/')
        return fs.save(image.name, image)
