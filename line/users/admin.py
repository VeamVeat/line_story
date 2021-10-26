from django.contrib import admin

from users.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff',)

    list_filter = ('first_name', 'last_name', 'email')

    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'age', 'phone', 'region']
