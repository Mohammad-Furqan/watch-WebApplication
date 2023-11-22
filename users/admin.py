from django.contrib import admin
from users.models import UserDetail
from django.contrib.auth.models import User
# Register your models here.


class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_first_name', 'get_last_name', 'get_email', 'phone_number', 'address')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user.first_name else 'N/A'

    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user.last_name else 'N/A'

    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email if obj.user.email else 'N/A'

    get_email.short_description = 'Email'

admin.site.register(UserDetail, UserDetailAdmin)


