from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path

from users.views import CustomActionView
from users.forms import ProfileAdminForm
from users.models import User, Profile, Wallet
from products.models import File


class WalletInline(admin.StackedInline):
    model = Wallet
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name',
                    'is_active', 'is_staff')
    list_display_links = ('email',)
    list_filter = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

    inlines = [WalletInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'phone', 'region', 'balance_user']
    readonly_fields = ('balance_user', 'file_image')
    change_form_template = 'admin/users/custom_change_form.html'

    form = ProfileAdminForm

    fieldsets = (
        (None, {
            'fields': ('user', 'age', 'phone', 'region', 'balance_user', 'picture', 'file_image'),
        }),
    )

    @staticmethod
    def file_image(obj):
        file_width = 100
        file_height = 100

        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.image.url,
            width=file_width,
            height=file_height,
        )
        )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['picture'] and request.user.is_superuser:
            file = form.cleaned_data['picture']
            profile_image = File.objects.get(id=obj.image.id)
            profile_image.image = file
            profile_image.save()
        return super(ProfileAdmin, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user__wallet')
        return queryset

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<path:object_id>/grant_money/',
                 self.admin_site.admin_view(CustomActionView.as_view()),
                 name='grant_money'),
        ]
        return my_urls + urls
