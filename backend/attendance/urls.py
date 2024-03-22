from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from attendance import views

router = DefaultRouter()
router.register('courses', views.CourseViewSet)

app_name = 'attendance'
urlpatterns = [
    path('', include(router.urls)),
    path(
        "attendance/history",
        views.AttendanceHistoryViewSet.as_view({'get': 'list'}),
        name="attendance-history",
    ),
]
