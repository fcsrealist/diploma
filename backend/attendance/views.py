"""
Views for the attendance APIs
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Course, Attendance, Student
from attendance import serializers
from attendance.logic import FaceRecognitionUseCase


class CourseViewSet(viewsets.ModelViewSet):
    """View for manage course APIs"""
    serializer_class = serializers.CourseSerializer
    queryset = Course.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'mark_attendance':
            return serializers.AttendanceCreateSerializer
        elif self.action == 'create' or self.action == 'update':
            return serializers.CourseCreateUpdateSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new course"""
        serializer.save(user=self.request.user, status=Course.StatusType.INACTIVE)

    @action(methods=["post"], detail=True, url_path='mark-attendance')
    def mark_attendance(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        face_recognition_use_case = FaceRecognitionUseCase(
            course=course,
            image=request.FILES['file']
        )

        face_recognition_use_case.execute()
        course.status = Course.StatusType.ACTIVE
        course.save()

        return Response(status=204)

    @action(methods=["post"], detail=True, url_path='end-session')
    def end_session(self, request, *args, **kwargs):
        course = self.get_object()

        course.status = Course.StatusType.INACTIVE
        course.save()

        return Response(status=204)


class AttendanceHistoryViewSet(viewsets.ModelViewSet):
    """View for manage course APIs"""
    serializer_class = serializers.AttendanceSerializer
    queryset = Attendance.objects.all().order_by("-id")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        course_id = int(self.request.query_params.get("course_id"))

        queryset = (self.filter_queryset(self.get_queryset())
                    .filter(course_id=course_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StudentSerializer
