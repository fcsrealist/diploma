"""Serializers for attendance APIs"""
from rest_framework import serializers

from core.models import (
    Course,
    Student,
    Attendance
)


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'name', 'photo')


class CourseSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'status', 'students']


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializers for the courses"""
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'student_ids']
        read_only_fields = ['id']

    def _attach_students(self, students_ids, course):
        for students_id in students_ids:
            course.students.add(Student.objects.get(id=students_id))

    def create(self, validated_data):
        """Create a recipe"""
        student_ids = validated_data.pop('student_ids', [])
        course = Course.objects.create(**validated_data)
        self._attach_students(student_ids, course)

        return course

    def update(self, instance, validated_data):
        """Update recipe"""
        student_ids = validated_data.pop('student_ids', None)
        if student_ids is not None:
            instance.students.clear()
            self._attach_students(student_ids, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AttendanceCreateSerializer(serializers.Serializer):
    file = serializers.FileField()


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y-%m-%d")


    class Meta:
        model = Attendance
        fields = ("id", "status", "student", "created_at")
