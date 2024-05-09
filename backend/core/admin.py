"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'name', 'is_active', 'is_staff', 'is_superuser'
            )
        }),
    )


class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'face_encoding' in form.base_fields:
            del form.base_fields['face_encoding']
        return form


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Course)
