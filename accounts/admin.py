from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import CustomUser

class CustomUSerAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = [
        "id", "email", "username", "is_superuser", "is_staff",
    ]
    
    add_fieldsets = (
        (None, {
            "classes" : ("wide",),
            "fields" : ("username", "email", "password1", "password2")
        }),
    )
     
admin.site.register(CustomUser, CustomUSerAdmin)