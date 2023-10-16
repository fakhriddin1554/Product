from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("email", "phone", "is_staff", "is_active",)
    list_filter = ("email", "phone", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "phone")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "phone", "password1", "password2", "is_staff",
                "is_active", "is_superuser", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email", "phone")
    ordering = ("email",)

admin.site.register(Profile)