from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from apps.accounts.models import User, UserLogs

from apps.accounts.forms import UserAdminCreationForm, UserAdminChangeForm


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    model = User

    list_display = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_administrator', 'is_operator', 'is_active']
    list_filter = ['is_superuser', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['last_login', 'date_joined']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff', 'is_administrator', 'is_operator',)}),
        ('Others', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_superuser', 'is_staff', 'is_administrator', 'is_operator')}
         ),
    )


admin.site.unregister(Group)


@admin.register(UserLogs)
class UserLogsAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'device', 'os', 'action', 'timestamp']
    search_fields = ['user__username', 'user__email']

    def has_add_permission(self, request):
        return False
