"""
Views for the attendance APIs
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.models import Course
from attendance import serializers


class CourseViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.CourseSerializer
    queryset = Course.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
